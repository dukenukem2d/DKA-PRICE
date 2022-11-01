"""
Модуль отправки прайс листа по gmail
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(sender: str, reciver: str, token: str, alias_sender: str, file_name: str) -> str:
    """
    Функция отправки прайс листа
    """
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, token)
        msg = MIMEMultipart()
        msg['From'] = alias_sender
        msg['To'] = reciver
        msg["Subject"] = file_name
        msg.attach(MIMEText('Price list'))

        with open(file_name, "rb") as f_table:
            file = MIMEApplication(f_table.read())

        file.add_header('content-disposition', 'attachment',
                        filename=file_name)
        msg.attach(file)

        server.sendmail(sender, reciver, msg.as_string())

        return "Message was sent"
    except smtplib.SMTPAuthenticationError as _ex:
        return f"{_ex}\nCheck you login or password"
