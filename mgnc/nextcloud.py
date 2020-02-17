import os
from datetime import datetime

from webdav3.client import Client

from mgnc import settings


def load_opts_from_env():
    return {
        "webdav_hostname": settings.NEXTCLOUD_WEBDAV_URL,
        "webdav_login": settings.NEXTCLOUD_USER,
        "webdav_password": settings.NEXTCLOUD_PASS,
        "verbose": settings.DEBUG,
    }


def new_client(options=None):
    if options is None:
        options = load_opts_from_env()
    client = Client(options)
    return client


def build_remote_path(inbox_dir, file_name):
    if inbox_dir is None:
        raise Exception("MGNC_INBOX_DIR must be set to a dir that exists in Nextcloud.")
    sanitized_name = os.path.basename(file_name)
    print(file_name, sanitized_name)
    if sanitized_name != file_name:
        raise Exception(
            "Possible directory traversal detected with filename: {}".format(file_name)
        )
    full_path = "{}/{}".format(inbox_dir, sanitized_name)
    print(full_path, os.path.abspath(full_path))
    if os.path.abspath(full_path) != full_path or not full_path.startswith(inbox_dir):
        raise Exception(
            "Possible directory traversal detected with filename: {}".format(file_name)
        )
    return full_path


def increment_filename(file_name):
    parts = file_name.rsplit(".", 1)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(parts) == 1:
        return "{} - {}".format(parts[0], stamp)
    else:
        return "{} - {}.{}".format(parts[0], stamp, parts[1])


def remote_path_for(client, inbox_path, file_name):
    remote_path = build_remote_path(inbox_path, file_name)
    max_checks = 10
    c = 0
    while client.check(remote_path) and c <= max_checks:
        remote_path = increment_filename(remote_path)
        c += 1
    if c == max_checks:
        raise Exception("Could not find unique name for path {}".format(file_name))

    return remote_path


def put_file(route, file_name, contents):
    client = new_client()
    inbox_path = route["remote_path"]
    remote_path = remote_path_for(client, inbox_path, file_name)
    client.upload_to(buff=contents, remote_path=remote_path)


if __name__ == "__main__":
    # client = new_client()
    # put_file("test.txt", "hello123")
    print(increment_filename("/foo"))
    print(increment_filename("/foo.pdf"))
    # client.execute_request("mkdir", 'directory_name')
