from bs4 import BeautifulSoup

from pyBCV.requests import get_content_page
from pyBCV.util import (
    TASAS_INFORMATIVAS_URL,
    PAGINA_PRINCIPAL_URL
)

def _get_rate_by_id(tag_id: str, soup: BeautifulSoup):
    return soup.find(id=tag_id).find("strong").text.strip().replace(',', '.')

def _get_time(soup: BeautifulSoup):
    date = soup.find("span", "date-display-single")
    return [date.text.strip().replace('  ', ' '), date.get("content").split('T')[0]]

def _get_rates_with_for(soup: BeautifulSoup, name: str = "td", attrs: str = None):
    return [str(x.text).strip() for x in soup.find_all(name, attrs)]

class Currency(object):
    """
    La clase Currency se utiliza para obtener los precios de los tipos de cambio \
    proporcionados por el Banco Central de Venezuela (BCV). \n
    - El método _load se encarga de obtener los datos de la página web y almacenarlos en el diccionario self.rates. \n
    - El método get_rate se utiliza para obtener los datos almacenados en el diccionario self.rates. Si se proporciona un código de moneda, devolverá el valor correspondiente para esa moneda. \n\n
    ```python
    import pyBCV

    currency = pyBCV.Currency()

    # Obtener todos los datos almacenados en el diccionario
    all_rates = currency.get_rate()
    print(all_rates)

    # Obtener el tipo de cambio para USD sin símbolo de moneda
    usd_rate = currency.get_rate(currency_code='USD', prettify=False)
    print(usd_rate)

    # Obtener la fecha de la última actualización
    last_update = currency.get_rate(currency_code='Fecha')
    print(last_update)
    ```
    """
    def _load(self) -> None:
        soup = BeautifulSoup(get_content_page(PAGINA_PRINCIPAL_URL), "html.parser")
        section_tipo_de_cambio_oficial = soup.find("div", "view-tipo-de-cambio-oficial-del-bcv")

        self.rates = {
            "EUR": _get_rate_by_id("euro", section_tipo_de_cambio_oficial),
            "CNY": _get_rate_by_id("yuan", section_tipo_de_cambio_oficial),
            "TRY": _get_rate_by_id("lira", section_tipo_de_cambio_oficial),
            "RUB": _get_rate_by_id("rublo", section_tipo_de_cambio_oficial),
            "USD": _get_rate_by_id("dolar", section_tipo_de_cambio_oficial),
            "Fecha": _get_time(section_tipo_de_cambio_oficial)
        }

    def get_rate(self, currency_code: str = None, prettify: bool = True):
        self._load()

        if not currency_code:
            return self.rates
        if currency_code not in self.rates:
            raise KeyError("Does not match any of the properties that were provided in the dictionary. Most information: https://github.com/fcoagz/pyBCV")
        
        return (self.rates[currency_code] if currency_code == "Fecha" 
                else f"Bs. {self.rates[currency_code]}" if prettify 
                else self.rates[currency_code])

class Bank(object):
    """
    La clase Bank en la librería pyBCV se utiliza para obtener información sobre los tipos de cambio de compra y venta de moneda extranjera \
    para los bancos disponibles en el sistema bancario del Banco Central de Venezuela (BCV). \n
    - La función _load de la clase Bank utiliza el módulo BeautifulSoup para extraer la información de las tasas informativas oficiales del BCV y almacenarla en un diccionario. \n
    - El método get_by_bank se utiliza para obtener la información de compra y venta de moneda extranjera para un banco específico o para todos los bancos disponibles. \n\n
    ```py
    import pyBCV

    bcv = pyBCV.Bank()
    bank_info = bcv.get_by_bank()
    print(bank_info)
    ```
    """
    def _load(self):
        section_tasas_informativas_oficial = BeautifulSoup(get_content_page(TASAS_INFORMATIVAS_URL), "html.parser")

        date_indicator = _get_rates_with_for(section_tasas_informativas_oficial, attrs = "views-field views-field-field-fecha-del-indicador")
        title_bank = _get_rates_with_for(section_tasas_informativas_oficial, attrs = "views-field views-field-views-conditional")
        rate_buys = _get_rates_with_for(section_tasas_informativas_oficial, attrs = "views-field views-field-field-tasa-compra")
        rate_sales = _get_rates_with_for(section_tasas_informativas_oficial, attrs = "views-field views-field-field-tasa-venta")

        self.banks = {}
        for i in range(10): # results: 10
            bank = {
                "Fecha": date_indicator[i],
                "Compra": f"Bs. {rate_buys[i]}",
                "Venta": f"Bs. {rate_sales[i]}",
            }
            self.banks[title_bank[i]] = bank

    def get_by_bank(self, bank_code=None, rate_or_sale=None):
        self._load()

        if not bank_code:
            return self.banks
        if bank_code not in self.banks:
            raise KeyError("Does not match any of the properties that were provided in the dictionary. Most information: https://github.com/fcoagz/pyBCV")
        
        return self.banks[bank_code][rate_or_sale] if rate_or_sale in self.banks[bank_code] else self.banks[bank_code]