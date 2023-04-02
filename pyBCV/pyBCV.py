import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

class Currency:
    def get_rate(self, currency_code=None):
        webSite = 'https://www.bcv.org.ve/'
        webResult = requests.get(webSite, verify=False)

        if webResult.status_code == 200: # OK!
            dataWeb = BeautifulSoup(webResult.content, 'html.parser')

            etiHTML = dataWeb.find_all('div', 'col-sm-12 col-xs-12')
            priceResult = []

            for eti in etiHTML:
                text = eti.find('strong')
                priceResult.append(text.text.strip().replace(',', '.'))

            rates = {
                'EUR' : f'Bs. {round(float(priceResult[-5]), 2)}',
                'CNY' : f'Bs. {round(float(priceResult[-4]), 2)}',
                'TRY' : f'Bs. {round(float(priceResult[-3]), 2)}',
                'RUB' : f'Bs. {round(float(priceResult[-2]), 2)}',
                'USD' : f'Bs. {round(float(priceResult[-1]), 2)}'
            }

            if not currency_code:
                return rates

            elif currency_code in rates:
                return rates[currency_code]