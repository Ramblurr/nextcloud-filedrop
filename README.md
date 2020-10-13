# nextcloud-filedrop (NCFD)

> Catch incoming email and save the attachments to nextcloud (or any webdav backend).


This project is a simple HTTP service that accepts multipart form POSTs
containing structured email data. It validates the attachments and uploads them
to a Nextcloud folder based on the recipient. You can have
"work-filedrop@yourdomain.com" route files to a separate folder than
"personal-filedrop@yourdomain.com".

This service supports two incoming email sources:

* [py-imap-to-http](https://github.com/Ramblurr/py-imap-to-http) *recommended,
  self-hosted imap watcher*
* Mailgun's [Inbound Routing](https://www.mailgun.com/inbound-routing/) *only
  available with monthly subscription plan, not available on the pay as you go plan*

## Get Going

Easiest way to get going is using docker.

1. Go fetch my fork of [py-imap-to-http](https://github.com/Ramblurr/py-imap-to-http)
2. Copy `docker-compose.sample.yml` to `docker-compose.yml`
3. Edit the `build: ../py-imap-to-http` line in the imap service to the location of the dir from step 1
4. Fill in your env vars.
5. `docker-compose up`

## Development

This project requires Python 3, and the python deps in `requirements.txt`. Using
a virtualenv is recommended.

```console
$ cp env-sample .env
# Edit .env with your values
$ pip install -r requirements.dev.txt
```

I recommend creating a specific nextcloud user to run this under rather than
your own account. Just share your inbox dirs to the user.

The settings should be self explanatory, except `NCFD_ROUTES`.

`NCFD_ROUTES` should be a comma separated list of email, path pairs which
themselves are separated by colons. Each email represents a recipient, and the
path is the remote path in Nextcloud that attachments from the recipient will be
uploaded to. This lets you run multiple filedrop emails from one instance.


### Run the thing

```console
$ python -m ncfd
```


## License

© 2020-present Casey Link. GNU Affero General Public License v3 or later

