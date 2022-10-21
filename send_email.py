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


def send_email(now, reciver, token):
    """
    Функция отправки прайс листа
    """
    sender = 'alexander.aleynikov@dkafze.com'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, token)
        # msg = MIMEText(message)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = reciver
        msg["Subject"] = f"Price List {now}"
        msg.attach(MIMEText(f"Price List {now}"))

        with open(f"Price_list-{now}.xlsx", "rb") as f_table:
            file = MIMEApplication(f_table.read())

        file.add_header('content-disposition', 'attachment',
                        filename=f"Price_list-{now}.xlsx")
        msg.attach(file)

        server.sendmail(sender, reciver, msg.as_string())

        return "Message was sent"
    except smtplib.SMTPAuthenticationError as _ex:
        return f"{_ex}\nCheck you login or password"
