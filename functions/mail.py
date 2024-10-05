import smtplib
from email.message import EmailMessage
from dark_fream.utils import get_settings

def send_email(sender_email, password, recipient_email, subject, body, host=get_settings('HOST'), port=get_settings('PORT')):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    server = smtplib.SMTP_SSL(host, port)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()


def send_html_email(sender_email, password, recipient_email, subject, html_body, host=get_settings('HOST'), port=get_settings('PORT')):
    msg = EmailMessage()
    msg.set_content(html_body, subtype='html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    server = smtplib.SMTP_SSL(host, port)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()
