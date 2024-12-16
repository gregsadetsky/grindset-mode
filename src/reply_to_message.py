import base64
from email.message import EmailMessage
from email.mime.text import MIMEText

from common import gmail_authenticate

MESSAGE_THREAD_TO_REPLY_TO = "193c738897460d9c"

GRIND_MESSAGE = """<audio controls><p>
<a href="https://gregsadetsky.github.io/grindset-mode/full.mp3">(click here)</a>
</p>
<source src="https://gregsadetsky.github.io/grindset-mode/full.mp3"></source>
</audio>
<br><br>I'm too busy grinding and there are {} messages in my inbox. Goodbye. x"""


# https://stackoverflow.com/a/41403459
def create_message_return_raw_base64(sender, to, subject, message_text, message_id):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    # print(sender + ", " + to + ", " + subject + ", " + message_text)
    message = MIMEText(message_text, "html")
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    message["References"] = message_id
    message["In-Reply-To"] = message_id
    # print(message)
    return base64.urlsafe_b64encode(message.as_string().encode()).decode()


def construct_and_reply_to_message(
    service, thread_id, nmb_remaining_messages_to_go_through
):
    # Retrieve the details of the thread
    thread = service.users().threads().get(userId="me", id=thread_id).execute()
    messages = thread["messages"][0]["payload"]["headers"]

    # Retrieve the metadata of the thread
    for k in messages:
        # print("k", k)
        if k["name"] == "To":
            recipient = k["value"]
        if k["name"] == "Subject":
            email_subject = k["value"]
        if k["name"] == "From":
            sender = k["value"]
        if k["name"] == "Message-Id" or k["name"] == "Message-ID":
            message_id = k["value"]

    # Constructing the reply message
    # message = EmailMessage()
    # message.set_content("This is a sample reply")
    # message["To"] = recipient
    # message["From"] = sender
    # message["Subject"] = email_subject
    # message["References"] = message_id
    # message["In-Reply-To"] = message_id
    # encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        "raw": create_message_return_raw_base64(
            recipient,
            sender,
            email_subject,
            GRIND_MESSAGE.format(nmb_remaining_messages_to_go_through),
            message_id,
        ),
        "threadId": thread_id,
    }
    # Sending the reply message to the thread
    send_message = (
        service.users().messages().send(userId="me", body=create_message).execute()
    )


if __name__ == "__main__":
    service = gmail_authenticate()
    construct_and_reply_to_message(service, MESSAGE_THREAD_TO_REPLY_TO)
