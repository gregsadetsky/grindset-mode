import base64
from email.mime.text import MIMEText

from common import gmail_authenticate

FROM = "lepetitg@gmail.com"
TO = "gs@gregsadetsky.com"


# https://stackoverflow.com/a/41403459
def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    print(sender + ", " + to + ", " + subject + ", " + message_text)
    message = MIMEText(message_text, "html")
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    print(message)
    return {"raw": base64.urlsafe_b64encode(message.as_string().encode()).decode()}


service = gmail_authenticate()
service.users().messages().send(
    userId="me",
    body=create_message(
        FROM,
        TO,
        "Inbox is full",
        "Hey, your inbox is full. Please <b>delete</b> some emails.",
    ),
).execute()
