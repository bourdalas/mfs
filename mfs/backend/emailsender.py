import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional


class EmailSender:
    def __init__(self, email_address: str, email_password: str, smtp_server: str = 'smtp.gmail.com', smtp_port: int = 465) -> None:
        self.email_address = email_address
        self.email_password = email_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, recipient_email: str, subject: str, body: str, attachments: Optional[List[str]] = None) -> None:
        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add the message body
        msg.attach(MIMEText(body, 'plain'))

        # Add any attachments
        if attachments is not None:
            for attachment in attachments:
                with open(attachment, 'rb') as file:
                    attach = MIMEApplication(file.read(), _subtype='pdf')
                    attach.add_header('Content-Disposition', 'attachment', filename=attachment)
                    msg.attach(attach)

        # Set up the SMTP server and send the email
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.email_address, self.email_password)
            server.sendmail(self.email_address, recipient_email, msg.as_string())



    def send_sign_up_email(self, user_name: str, user_email: str):
        body = f"""
        Hello {user_name}!
        Welcome to MFS!

        https://www.youtube.com/watch?v=ds7FIZy7Ds0
        Support workers strikes and keep on grooving!
        """
        self.send_email(
            recipient_email=user_email, 
            subject="Welcome to MFS!", 
            body=body
            )
