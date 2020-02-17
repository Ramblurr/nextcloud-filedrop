import os
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()


def get_env(key, default=None):
    return os.environ.get(key, default)


def parse_routes(route_defs):
    if route_defs is None or len(route_defs) == 0:
        raise Exception("env var MGNC_ROUTES must be defined. See README.md")
    pairs = route_defs.split(",")
    routes = []
    for p in pairs:
        rec, path = p.split(":")
        if not path.startswith("/"):
            path = "/" + path
        routes.append({"recipient": rec, "remote_path": path})
    return routes


NEXTCLOUD_WEBDAV_URL = get_env("MGNC_NEXTCLOUD_WEBDAV_URL")
NEXTCLOUD_USER = get_env("MGNC_NEXTCLOUD_USER")
NEXTCLOUD_PASS = get_env("MGNC_NEXTCLOUD_PASS")
DEBUG = get_env("DEBUG", "false").lower() in ["1", "true", "yes"]
INBOX_DIR = get_env("MGNC_INBOX_DIR")
MAX_ATTACHMENT_BYTES = int(get_env("MGNC_MAX_ATTACHMENT_BYTES", 25 * 1024 * 1024))
ROUTES = parse_routes(get_env("MGNC_ROUTES"))

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)
