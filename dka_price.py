"""
sdsdsdsdsdsds
"""
import sys
import os
from datetime import date
from dotenv import load_dotenv, find_dotenv
from formating import formating
from price_exctraction import exctraction
from send_email import send_email

load_dotenv(find_dotenv())

customer_id = sys.argv[1]
reciver = sys.argv[2]
now = date.today()
FILE = 'price_list.xlsx'
username = os.getenv('USERNAME_REPORT_SERVER')
password = os.getenv('PASSWORD_REPORT_SERVER')
sender = os.getenv('SENDER')
token = os.getenv('TOKEN_GMAIL')

def main():
    """
    Главная функция
    """
    print('HI')

exctraction(customer_id,now,username,password)
print('Exctraction DONE')
formating(FILE,customer_id,now)
send_email(now, sender, reciver, token)


if __name__ == "__main__":
    print("Тест функции ", main())
