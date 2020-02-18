from logging import getLogger
from email.utils import parseaddr

from flask import abort, request, make_response, send_file, Flask
from werkzeug.utils import secure_filename
import dateutil.parser

from ncfd.nextcloud import put_file
from ncfd import settings

app = Flask("nextcloud-filedrop")
app.config.MAX_CONTENT_LENGTH = settings.MAX_ATTACHMENT_BYTES
logger = getLogger(__name__)

EXTENSIONS = {
    "TEXT": ["txt", "md"],
    "DOCUMENT": [
        "pdf",
        "rtf",
        "odf",
        "ods",
        "odt",
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
    for route in settings.ROUTES:
        if recipient == route["recipient"]:
            return route
    logger.info("Unknown recipient {}".format(recipient))
    return False


def get_sender(values):
    return request.values["from"]


def get_recipient(values):
    opts = ["to", "recipient"]
    for opt in opts:
        if opt in request.values:
            return request.values[opt]
    raise Exception("Missing recipient")


def get_date(values):
    opts = ["date", "Date"]
    for opt in opts:
        if opt in request.values:
            return request.values[opt]
    raise Exception("Missing date")


@app.route("/", methods=["POST"])
def email_receiver():
    sender = get_sender(request.values)
    recipient = get_recipient(request.values)
    route = get_allowed_recipient(recipient)
    if not route:
        return make_response("NOT ALLOWED RECIPIENT", 406)

    files = request.files.values()
    attachments = [att for att in files if is_file_allowed(att.filename)]
    if len(attachments) <= 0:
        logger.info(
            "email received from {}. but with no valid attachments.".format(sender)
        )
        return make_response("no attachments", 200)

    logger.info("processing {} attachments from {}".format(len(attachments), sender))
    logger.debug(request.values)
    email_date = dateutil.parser.isoparse(get_date(request.values))
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
