from typing import Any

import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

class Currency:
    def get_rate(self, currency_code=None) -> dict[str, str] | str:
        response = requests.get('https://www.bcv.org.ve/', verify=False)

        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.content, 'html.parser')

            rates_of_cambie = []
            date_valid = []

            for i in soup.find_all('div', 'col-sm-12 col-xs-12'):
                rates_of_cambie.append(i.find('strong').text.strip().replace(',', '.'))
            for x in soup.find('div', 'pull-right dinpro center'):
                date_valid.append(x.text.strip())

            rates = {
                'EUR': f'Bs. {rates_of_cambie[-5]}',
                'CNY': f'Bs. {rates_of_cambie[-4]}',
                'TRY': f'Bs. {rates_of_cambie[-3]}',
                'RUB': f'Bs. {rates_of_cambie[-2]}',
                'USD': f'Bs. {rates_of_cambie[-1]}',
                date_valid[0].replace(':', ''): date_valid[1].replace('  ', ' ')
            }

            if not currency_code:
                return rates
            
            elif currency_code in rates:
                return rates[currency_code]
    
class Bank:
    def get_by_bank(self, bank_code=None, rate_or_sale=None) -> dict[Any, dict[str, str]] | str | dict[str, str]:
        response = requests.get('https://www.bcv.org.ve/tasas-informativas-sistema-bancario', verify=False)

        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.content, 'html.parser')

            date_indicator = []
            title_bank = []
            rate_buys = []
            rate_sales = []

            for i in soup.find_all('td', 'views-field views-field-field-fecha-del-indicador'):
                date_indicator.append(i.text.strip())
            for j in soup.find_all('td', 'views-field views-field-views-conditional'):
                title_bank.append(j.text.strip())
            for k in soup.find_all('td', 'views-field views-field-field-tasa-compra'):
                rate_buys.append(k.text.strip().replace(',', '.'))
            for e in soup.find_all('td', 'views-field views-field-field-tasa-venta'):
                rate_sales.append(e.text.strip().replace(',', '.'))
            
            bank = {
                title_bank[0]: {
                'Fecha': date_indicator[0],
                'Compra': f'Bs. {rate_buys[0]}',
                'Venta': f'Bs. {rate_sales[0]}'
                },
                title_bank[1]: {
                'Fecha': date_indicator[1],
                'Compra': f'Bs. {rate_buys[1]}',
                'Venta': f'Bs. {rate_sales[1]}'
                },
                title_bank[2]: {
                'Fecha': date_indicator[2],
                'Compra': f'Bs. {rate_buys[2]}',
                'Venta': f'Bs. {rate_sales[2]}'
                },
                title_bank[3]: {
                'Fecha': date_indicator[2],
                'Compra': f'Bs. {rate_buys[2]}',
                'Venta': f'Bs. {rate_sales[3]}'
                },
            }
            
            if not bank_code:
                return bank

            elif rate_or_sale in bank[bank_code]:          
                return bank[bank_code][rate_or_sale]
              
            elif bank_code in bank:
                return bank[bank_code]