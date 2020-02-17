# mailgun-nextcloud

> Catch incoming email from mailgun and save the attachments to nextcloud (or any webdav backend).


## Get Going

This project requirs Python 3, and the python deps in `requirements.txt`. Using
a virtualenv is recommended.

### Setup 
```
cp env-sample .env
# Edit .env with your values
pip install -r requirements.dev.txt
```

I recommend creating a specific nextcloud user to run this under rather than your own account. Just share your inbox dirs to the user.

The settings should be self explanatory, except `MGNC_ROUTES`.

`MGNC_ROUTES` should be a comma separated list of email, path pairs which themselves are separated by colons. Each email represents a recipient, and the path is the remote path in Nextcloud that attachments from the recipient will be uploaded to. This lets you run multiple filedrop emails from one instance.

### Run the thing

```
python -m mgnc
```


# License

© 220 Casey Link. GNU Affero General Public License v3 or later

