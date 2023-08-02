import os

def checking_host(ip_address:str):
    HOST_UP  = True if os.system("ping -c 1 " + f"{ip_address} 1>/dev/null") == 0 else False
    if HOST_UP is True:
        print("VPN connected")
        return
    raise ValueError("Pls connect VPN comapny")

if __name__ == "__main__":
    checking_host("192.168.1.106")

