from common import gmail_authenticate

INBOX_QUERY = "in:inbox"


def get_messages_from_inbox(service):
    result = service.users().messages().list(userId="me", q=INBOX_QUERY).execute()
    messages = []
    if "messages" in result:
        messages.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        result = (
            service.users()
            .messages()
            .list(userId="me", q=INBOX_QUERY, pageToken=page_token)
            .execute()
        )
        if "messages" in result:
            messages.extend(result["messages"])
    return messages


def get_all_unique_thread_ids_from_inbox(service):
    inbox_messages = get_messages_from_inbox(service)
    all_thread_ids = set()
    for msg in inbox_messages:
        all_thread_ids.add(msg["threadId"])
    return all_thread_ids


if __name__ == "__main__":
    service = gmail_authenticate()
    inbox_messages = get_messages_from_inbox(service)

    # we only want the count of the unique threads, not the count of all messages
    all_thread_ids = set()
    for msg in inbox_messages:
        all_thread_ids.add(msg["threadId"])
    print(f"Found {len(all_thread_ids)} unique threads in your inbox.")

    # get emails that match the query you specify from the command lines
    # results = search_messages(service, sys.argv[1])
    # print(f"Found {len(results)} results.")
    # # for each email matched, read it (output plain/text to console & save HTML and attachments)
    # for msg in results:
    #     read_message(service, msg)
