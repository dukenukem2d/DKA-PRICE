"""
Модуль отправки прайс листа по gmail
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
# from datetime import date

# now = date.today()

# reciver = 'nazirullo.negmatov@dkafze.com'


def send_email(sender, reciver, token, alias_sender, file_):
    """
    Функция отправки прайс листа
    """
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, token)
        # msg = MIMEText(message)
        msg = MIMEMultipart()
        msg['From'] = alias_sender
        msg['To'] = reciver
        msg["Subject"] = file_
        msg.attach(MIMEText('Price list'))

        with open(file_, "rb") as f_table:
            file = MIMEApplication(f_table.read())

        file.add_header('content-disposition', 'attachment',
                        filename=file_)
        msg.attach(file)

        server.sendmail(sender, reciver, msg.as_string())

        return "Message was sent"
    except smtplib.SMTPAuthenticationError as _ex:
        return f"{_ex}\nCheck you login or password"
