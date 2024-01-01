import requests

requests.packages.urllib3.disable_warnings()

def _ensure_200_response(url: str) -> requests.Response:
    response = requests.get(url, verify=False)
    response.raise_for_status()

    return response

p = _ensure_200_response('https://www.bcv.org.ve/cambiaria/export/tasas-informativas-sistema-bancario')
from bs4 import BeautifulSoup

soup = BeautifulSoup(p.content, "html.parser")
for x in soup.find_all('tr'):
    print(x.find_all('td'))