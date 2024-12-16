import time

from common import gmail_authenticate
from how_many_emails_in_my_inbox import get_all_unique_thread_ids_from_inbox
from reply_to_message import construct_and_reply_to_message

service = gmail_authenticate()
initial_thread_ids = get_all_unique_thread_ids_from_inbox(service)
# print(initial_thread_ids)
print("found", len(initial_thread_ids), "threads in inbox, starting loop")


def deal_with_new_thread_id(thread_id):
    construct_and_reply_to_message(service, thread_id, len(initial_thread_ids))

    # remove the 'INBOX' label to archive the thread
    service.users().threads().modify(
        userId="me", id=thread_id, body={"removeLabelIds": ["INBOX"]}
    ).execute()


while True:
    all_new_thread_ids = get_all_unique_thread_ids_from_inbox(service)
    # are there any new threads?
    new_thread_ids = list(set(all_new_thread_ids) - set(initial_thread_ids))

    for thread_id in new_thread_ids:
        print("dealing with thread id:", thread_id)
        deal_with_new_thread_id(thread_id)

    print("sleeping...")
    time.sleep(30)
