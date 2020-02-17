import os
from setuptools import setup, find_packages

setup(
    name="mailgun-nextcloud",
    description="Save attachments from emails to Nextcloud",
    long_description=open("README.md").read(),
    url="",
    version="0.0.1",
    author="Casey Link",
    author_email="unnamedrambler@gmail.com",
    packages=find_packages(exclude=["ez_setup"]),
    install_requires=open(
        os.path.join(os.path.dirname(__file__), "requirements.txt")
    ).readlines(),
    entry_points={"console_scripts": ["mailgun-nextcloud = mgnc.__main__:main"]},
    license="AGPL3",
)
