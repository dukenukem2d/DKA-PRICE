import sys
import os
from formating import formating
from price_exctraction import exctraction
from send_email import send_email
from datetime import date
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

customer_id = sys.argv[1]
reciver = sys.argv[2]
now = date.today()
file = 'price_list.xlsx'
username = os.getenv('USERNAME_REPORT_SERVER')
password = os.getenv('PASSWORD_REPORT_SERVER')
token = os.getenv('TOKEN_GMAIL')

def main():
    print('HI')

exctraction(customer_id,now,username,password)
print('Exctraction DONE')
formating(file,customer_id,now)
send_email(now, reciver, token)


if __name__ == "__main__":
    print("Данный код выполняется т.к. модуль был запущен автономно (как скрипт) и не будет выполнен при импорте.")
    print("Тест функции ", main())