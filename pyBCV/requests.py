import requests
from requests import Response

requests.packages.urllib3.disable_warnings()

def ensure_200_response_and_return_content(response: Response) -> bytes:
    if not response.status_code == requests.codes.ok:
            raise ValueError("Error de comunicación Bcv.")
    return response.content

def get_content_page(url: str) -> bytes:
    return ensure_200_response_and_return_content(
        requests.get(url=url)
    )