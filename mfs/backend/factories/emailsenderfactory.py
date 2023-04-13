

import os

from dotenv import find_dotenv, load_dotenv

from mfs.backend.emailsender import EmailSender


def create_env_email_sender() -> EmailSender:
    load_dotenv(find_dotenv())

    return EmailSender(email_address=os.environ["MFS_EMAIL_ADDRESS"], email_password=os.environ["MFS_EMAIL_APP_PASSWORD"])