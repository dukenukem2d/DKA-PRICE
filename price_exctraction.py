import requests
from requests_ntlm import HttpNtlmAuth
# import os
# from datetime import date
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())

# now = date.today()
# customer_id = '0011'
# user = os.getenv('USERNAME')
# pass_ = os.getenv('PASSWORD')

def exctraction(customer_id, now, username, password):
    query = f'''http://192.168.1.104/ReportServer/Pages/ReportViewer.aspx?%2fDynamicsAX%2fCustPriceList.PrecisionDesign&CustPriceList_CustAccount={customer_id}&CustPriceList_PerDate={now}&CustPriceList_CurrencyCode=usd&CustPriceList_DataArea=dka&rs:Command=Render&rs:Format=Excel'''

    request = requests.get(query,auth=HttpNtlmAuth(username, password))

    # session = requests.Session()
    # session.auth = HttpNtlmAuth(username, password,)
    # request = session.get(query)


    if request.status_code == 200:
        with open('price_list.xlsx', 'wb') as out:
            for bits in request.iter_content():
                out.write(bits)

def main():
    exctraction(customer_id, now)

if __name__ == "__main__":
    main()