import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

class Currency:
    def get_rate(self, currency_code=None):
        webSite = 'https://www.bcv.org.ve/'
        webResult = requests.get(webSite, verify=False)

        if webResult.status_code == 200: # OK!
            dataWeb = BeautifulSoup(webResult.content, 'html.parser')

            label_html = dataWeb.find_all('div', 'col-sm-12 col-xs-12')
            priceResult = []

            for i in label_html:
                x = i.find('strong')
                priceResult.append(x.text.strip().replace(',', '.'))

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
            
    
    def get_by_bank(self, bank_code=None, rate_or_sale=None):
        webSite = 'https://www.bcv.org.ve/tasas-informativas-sistema-bancario'
        webResult = requests.get(webSite, verify=False)

        if webResult.status_code == 200: #OK!
            dataWeb = BeautifulSoup(webResult.content, 'html.parser')

            label_html_date = dataWeb.find_all('td', 'views-field views-field-field-fecha-del-indicador')
            label_html_bank = dataWeb.find_all('td', 'views-field views-field-views-conditional')
            label_html_ratebuys = dataWeb.find_all('td', 'views-field views-field-field-tasa-compra')
            label_html_ratesales = dataWeb.find_all('td', 'views-field views-field-field-tasa-venta')

            dateIndicator = []
            titleBank = []
            rateBuys = []
            rateSales = []

            for w in label_html_date:
                dateIndicator.append(w.text.strip())
            for x in label_html_bank:
                titleBank.append(x.text.strip())
            for y in label_html_ratebuys:
                rateBuys.append(y.text.strip().replace(',', '.'))
            for z in label_html_ratesales:
                rateSales.append(z.text.strip().replace(',', '.'))

            titleBank[3] = titleBank[3].replace('é', 'e')

            bank = {
                titleBank[0]: {
                'Fecha' : f'{dateIndicator[0]}',
                'Compra' : f'Bs. {round(float(rateBuys[0]), 2)}',
                'Venta' : f'Bs. {round(float(rateSales[0]), 2)}'
                },
                titleBank[1]: {
                'Fecha' : f'{dateIndicator[1]}',
                'Compra' : f'Bs. {round(float(rateBuys[1]), 2)}',
                'Venta' : f'Bs. {round(float(rateSales[1]), 2)}'
                },
                titleBank[2]: {
                'Fecha' : f'{dateIndicator[2]}',
                'Compra' : f'Bs. {round(float(rateBuys[2]), 2)}',
                'Venta' : f'Bs. {round(float(rateSales[2]), 2)}'
                },
                titleBank[3]: {
                'Fecha' : f'{dateIndicator[3]}',
                'Compra' : f'Bs. {round(float(rateBuys[3]), 2)}',
                'Venta' : f'Bs. {round(float(rateSales[3]), 2)}'
                },
                titleBank[4]: {
                'Fecha' : f'{dateIndicator[4]}',
                'Compra' : f'Bs. {round(float(rateBuys[4]), 2)}',
                'Venta' : f'Bs. {round(float(rateSales[4]), 2)}'
                },
            }
            
            if not bank_code:
                return bank

            elif rate_or_sale in bank[bank_code]:          
                return bank[bank_code][rate_or_sale]
              
            elif bank_code in bank:
                return bank[bank_code]