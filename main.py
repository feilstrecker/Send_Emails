import smtplib
from email.message import Message
import io
import os

def send_emails(subject, from_email, password):
    message = get_message()
    emails = get_emails()

    s = login(from_email, password)

    for email in emails:
        msg = email_body(subject, from_email, email, message)
        s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
        print(f"sent to [{msg['To']}] with success!")

def email_body(subject, from_email, to, message):
    msg = Message()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)
    return msg

def get_message():
    message = ''
    message_paragraphs = []

    with io.open('config\\msg.txt', 'r', encoding='utf-8') as arc:
        dirty_message = arc.read()
        for p in dirty_message.split('\n'):
            message_paragraphs.append(f"<p>{p}<p>")
        for msg in message_paragraphs:
            message += f'{msg}\n'
        return message

def get_emails():
    with open('config\\send_to.txt', 'r') as arc:
        emails = arc.read().split('\n')
        return emails

def login(from_email, password):
    try:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(from_email, password)
        return s
    except smtplib.SMTPAuthenticationError:
        return False

def menu():
    while True:
        from_email = input('from email: ')
        password = input('password(get it from password manager): ')
        os.system('cls')
        verify_credentials = login(from_email, password)
        if verify_credentials == False:
            print('login error, try again.')
        else:
            print('logged with success.')
            subject = input('subject: ')
            send_emails(subject=subject, from_email=from_email, password=password)

menu()