import imaplib
import email

def fetch_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('architmaheshwari0@gmail.com', 'xyz')
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')

    email_ids = data[0].split()[-10:]

    for email_id in reversed(email_ids):
        result, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]

        # Parse the email
        msg = email.message_from_bytes(raw_email)

        # Extract subject
        subject = msg.get('Subject')

        # Extract sender
        sender = msg.get('From')

        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # Skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body_bytes = part.get_payload(decode=True)  # Decode from base64
                    body = body_bytes.decode()  # Decode bytes to string
                    break
        else:
            body_bytes = msg.get_payload(decode=True)
            body = body_bytes.decode()

        print(f"Subject: {subject}")
        print(f"From: {sender}")
        print(f"Body: {body}\n")

    mail.close()

    mail.logout()


if __name__ == '__main__':
    fetch_mail()
