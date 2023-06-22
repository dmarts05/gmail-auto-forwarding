"""Module to scrape the forwarding code from emails."""

import email as em
import imaplib

from gmail_auto_forwarding.utils.logger import setup_logger

from .constants import EMAIL_FORMAT, FORWARDING_CODE_FROM_EMAIL, IMAP_GMAIL_URL
from .helpers import get_body_of_email

logger = setup_logger(logger_name=__name__)


def scrape_forwarding_code(email: str, app_password: str) -> str:
    """
    Scrapes the forwarding code from verification emails.

    Args:
        email: Email address of the account to scrape.
        app_password: App password of the account to scrape.

    Returns:
        Forwarding code.
    """
    mail = imaplib.IMAP4_SSL(IMAP_GMAIL_URL)
    mail.login(email, app_password)
    mail.select("inbox")

    # Search for forwarding code emails
    _, msg_ids = mail.search(None, "FROM", FORWARDING_CODE_FROM_EMAIL)

    # Iterate over all the emails
    code = ""
    for msg_id in msg_ids[0].split():
        # Fetch the email data (RFC822) for the given ID
        _, msg_data = mail.fetch(msg_id, EMAIL_FORMAT)

        # Iterate over all the responses
        for response in msg_data:
            # Check if the response is a tuple (contains the email data)
            if isinstance(response, tuple):
                msg = em.message_from_bytes(response[1])
                body = get_body_of_email(msg)
                logger.debug(f"Body of email: {body}")

                # Extract the forwarding code
                code = body.split(": ")[1].split("\n")[0]
                logger.debug(f"Forwarding code: {code}")

                # Trash email
                mail.store(msg_id, "+X-GM-LABELS", "\\Trash")

    mail.close()
    return code
