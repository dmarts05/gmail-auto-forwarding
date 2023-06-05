from email.message import Message


def get_body_of_email(msg: Message) -> str:  # type: ignore
    """
    Get the body of an email.

    Args:
        msg: Email message.

    Returns:
        Body of the email.
    """
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # Skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in cdispo:
                return part.get_payload(decode=True).decode("utf-8")
    else:
        return msg.get_payload(decode=True).decode("utf-8")
