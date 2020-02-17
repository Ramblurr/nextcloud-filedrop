from logging import getLogger
from email.utils import parseaddr

from flask import abort, request, make_response, send_file, Flask
from werkzeug.utils import secure_filename
import dateutil.parser

from mgnc.nextcloud import put_file
from mgnc import settings

app = Flask("mailgun_nextcloud")
app.config.MAX_CONTENT_LENGTH = settings.MAX_ATTACHMENT_BYTES
logger = getLogger(__name__)

EXTENSIONS = {
    "TEXT": ["txt", "md"],
    "DOCUMENT": [
        "rtf",
        "odf",
        "ods",
        "gnumeric",
        "abw",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "xlsb",
    ],
    "IMAGE": ["jpg", "jpeg", "jpe", "png", "gif", "svg", "bmp", "webp"],
    "AUDIO": ["wav", "mp3", "aac", "ogg", "oga", "flac"],
    "DATA": ["csv", "ini", "json", "plist", "xml", "yaml", "yml"],
    "SCRIPT": ["js", "php", "pl", "py", "rb", "sh"],
    "ARCHIVE": ["gz", "bz2", "zip", "tar", "tgz", "txz", "7z"],
}

ALL_EXTENSIONS = (
    EXTENSIONS["TEXT"]
    + EXTENSIONS["DOCUMENT"]
    + EXTENSIONS["IMAGE"]
    + EXTENSIONS["AUDIO"]
    + EXTENSIONS["DATA"]
    + EXTENSIONS["ARCHIVE"]
)


def is_file_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALL_EXTENSIONS


def get_allowed_recipient(recipient):
    print(settings.ROUTES)
    for route in settings.ROUTES:
        if recipient == route["recipient"]:
            return route
    logger.info("Unknown recipient {}".format(recipient))
    return False


@app.route("/", methods=["POST"])
def email_receiver():
    attachment_count = int(request.values["attachment-count"])
    if attachment_count <= 0:
        logger.info("email received from {}. but with attachments.".format(sender))
        return make_response("no attachments", 200)
    sender = request.values["from"]
    recipient = request.values["recipient"]
    route = get_allowed_recipient(recipient)
    if not route:
        return make_response("NOT ALLOWED RECIPIENT", 406)

    files = request.files.values()
    attachments = [att for att in files if is_file_allowed(att.filename)]

    logger.info("processing {} attachments from {}".format(len(attachments), sender))
    email_date = dateutil.parser.parse(request.values["Date"])
    date_prefix = email_date.strftime("%Y-%m-%d")
    sender_email = parseaddr(sender)[1]
    for attachment in attachments:
        filename = "{} - {} - {}".format(date_prefix, sender_email, attachment.filename)
        res = put_file(route, filename, attachment)
        if not res:
            make_response("Upload failed", 500)
            logger.info("Uploading attachments failed")
    return make_response("OK", 200)


@app.route("/", methods=["GET"])
def email_receiver_get():
    return make_response("At the ready.", 200)
