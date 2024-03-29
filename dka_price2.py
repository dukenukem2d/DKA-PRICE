import argparse
import os

from pathlib import Path
from datetime import date
from dotenv import find_dotenv, load_dotenv

from formating import formating
from price_exctraction import exctraction
from send_email import send_email
from file_manipulation import remove_old_files

load_dotenv(find_dotenv())

customer_id = os.getenv('DEFAULT_CUSTOMER_ID')
reciver = os.getenv('DEFAULT_RECIVER')
date_today = date.today()
username = os.getenv('USERNAME_REPORT_SERVER')
password = os.getenv('PASSWORD_REPORT_SERVER')
sender = os.getenv('SENDER')
alias_sender = os.getenv('SENDER_ALIAS')
token = os.getenv('TOKEN_GMAIL')
# Define the command line arguments
parser = argparse.ArgumentParser(description='Download and send a file.')
parser.add_argument('customer_id', nargs='?',
                    default=None, help='the customer ID')
parser.add_argument('email', nargs='?', default=None,
                    help='the email address to send the file to')
args = parser.parse_args()

# Define the URL of the file to download
query = f'''http://192.168.1.104/ReportServer/Pages/ReportViewer.aspx?%2fDynamicsAX%2fCustPriceList.PrecisionDesign&CustPriceList_CustAccount={customer_id}&CustPriceList_PerDate={date_today}&CustPriceList_CurrencyCode=usd&CustPriceList_DataArea=dka&rs:Command=Render&rs:Format=Excel'''  # pylint: disable=line-too-long


if args.customer_id is None:
    # No arguments were provided, just download the file
    file_excel = f'Price_list-{customer_id}-{date_today}.xlsx'
    path = Path(file_excel)
    if path.is_file():
        print("File exist")
    else:
        formating(exctraction(query, username, password), customer_id, date_today)
        print('File downloaded successfully.')
elif args.email is None:
    customer_id = args.customer_id
    file_excel = f'Price_list-{customer_id}-{date_today}.xlsx'
    path = Path(file_excel)
    if path.is_file():
        send_email(sender, reciver, token, alias_sender, file_excel)  # type: ignore
        print("File exists and sent to default email id")
    else:
        formating(exctraction(query, username, password), customer_id, date_today)
        send_email(sender, reciver, token, alias_sender, file_excel)  # type: ignore
        print('File sent to default email address.')
else:
    # Both the customer ID and email address were provided, send the file to the specified email address
    customer_id = args.customer_id
    reciver = args.email
    file_excel = f'Price_list-{customer_id}-{date_today}.xlsx'
    path = Path(file_excel)
    if path.is_file():
        send_email(sender, reciver, token, alias_sender, file_excel)  # type: ignore
        print("File exists and sent to default email id")
    else:
        formating(exctraction(query, username, password), customer_id, date_today)
        send_email(sender, reciver, token, alias_sender, file_excel)  # type: ignore
        print('File sent to specified email address.')

remove_old_files(date_today)
