"""
Выгрузка и отправка прайс листа на почту
"""
import os
import sys
from datetime import date

from dotenv import find_dotenv, load_dotenv

from formating import formating
from price_exctraction import exctraction
from send_email import send_email
from file_manipulation import remove_old_files

load_dotenv(find_dotenv())

customer_id = os.getenv('DEFAULT_CUSTOMER_ID')
reciver = os.getenv('DEFAULT_RECIVER')
if sys.argv[1:]:
    customer_id = sys.argv[1]
    reciver = sys.argv[2]
date_today = date.today()
username = os.getenv('USERNAME_REPORT_SERVER')
password = os.getenv('PASSWORD_REPORT_SERVER')
sender = os.getenv('SENDER')
alias_sender = os.getenv('SENDER_ALIAS')
token = os.getenv('TOKEN_GMAIL')

query = f'''http://192.168.1.104/ReportServer/Pages/ReportViewer.aspx?%2fDynamicsAX%2fCustPriceList.PrecisionDesign&CustPriceList_CustAccount={customer_id}&CustPriceList_PerDate={date_today}&CustPriceList_CurrencyCode=usd&CustPriceList_DataArea=dka&rs:Command=Render&rs:Format=Excel'''  # pylint: disable=line-too-long


def main():
    """
    Главная функция
    """
    file_excel = f'Price_list-{customer_id}-{date_today}.xlsx'
    formating(exctraction(query, username, password), customer_id, date_today)
    send_email(sender, reciver, token, alias_sender,
               file_excel)  # type: ignore
    remove_old_files(date_today)


if __name__ == "__main__":
    print("Запуск приложения ", main())
