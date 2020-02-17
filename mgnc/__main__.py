import os

from mgnc.app import app
from mgnc import settings


def main():
    app.run(debug=settings.DEBUG, host="127.0.0.1", port=3000)


if __name__ == "__main__":
    main()
