import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import socket

def send_email(recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('SMTP_EMAIL')
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(os.getenv('SMTP_SERVER'), 587, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.login(os.getenv('SMTP_EMAIL'), os.getenv('SMTP_PASSWORD'))
                server.send_message(msg)
                print("Yes, on port 587")
        except:
            with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), 465, timeout=10) as server:
                server.login(os.getenv('SMTP_EMAIL'), os.getenv('SMTP_PASSWORD'))
                server.send_message(msg)
                print("Yes, on port 465")


        print(f"✅ Email sent to {recipient_email}")
        return True

    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {str(e)}")
    except socket.timeout:
        print(f"❌ Connection timeout")
    except Exception as e:
        print(f"❌ General error: {str(e)}")

    return False
