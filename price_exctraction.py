"""
Модуль загрузки прайс листа с сервера отчетов
"""
#from typing import Union
import requests
from requests_ntlm import HttpNtlmAuth # type: ignore


#def exctraction(query: str, username: Union[str, None], password: Union[str, None]) -> bytes:
def exctraction(query: str, username: str, password: str) -> bytes:
    """
    Функция загрузки прайс листа
    """
    request = requests.get(query, auth=HttpNtlmAuth(username, password))

    if request.status_code == 200:
        return request.content
    else:
        print("Use company VPN")
