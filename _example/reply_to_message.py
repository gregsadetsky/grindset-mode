import base64
from email.message import EmailMessage
from email.mime.text import MIMEText

from common import gmail_authenticate, OUR_EMAIL

FROM = OUR_EMAIL
MESSAGE_THREAD_TO_REPLY_TO = "193c738897460d9c"


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

# Retrieve the details of the thread
thread = (
    service.users().threads().get(userId="me", id=MESSAGE_THREAD_TO_REPLY_TO).execute()
)
messages = thread["messages"][0]["payload"]["headers"]

# Retrieve the metadata of the thread
for k in messages:
    print("k", k)
    if k["name"] == "To":
        recipient = k["value"]
    if k["name"] == "Subject":
        email_subject = k["value"]
    if k["name"] == "From":
        sender = k["value"]
    if k["name"] == "Message-Id":
        message_id = k["value"]

# Constructing the reply message
message = EmailMessage()
message.set_content("This is a sample reply")
message["To"] = recipient
message["From"] = sender
message["Subject"] = email_subject
message["References"] = message_id
message["In-Reply-To"] = message_id

encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

create_message = {"raw": encoded_message, "threadId": MESSAGE_THREAD_TO_REPLY_TO}
# Sending the reply message to the thread
send_message = (
    service.users().messages().send(userId="me", body=create_message).execute()
)
