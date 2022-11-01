"""
Модуль загрузки прайс листа с сервера отчетов
"""
import requests
from requests_ntlm import HttpNtlmAuth # type: ignore


def exctraction(query: str, username: str, password: str) -> bytes:
    """
    Функция загрузки прайс листа
    """
    request = requests.get(query, auth=HttpNtlmAuth(username, password))

    # if request.status_code == 200:
    #     with open('price_list.xlsx', 'wb') as out:
    #         for bits in request.iter_content():
    #             out.write(bits)
    return request.content
