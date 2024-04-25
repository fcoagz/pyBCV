from typing import Union
from bs4 import BeautifulSoup
from babel import dates

from ._requests import _ensure_200_response

def _get_time(soup: BeautifulSoup) -> str:
    date = soup.find("span", "date-display-single").get('content')
    response = dates.parse_date(date.split('T')[0])

    return dates.format_date(response, format='full', locale='es_US').capitalize()

def _get_rate_by_id(id: str, soup: BeautifulSoup) -> str:
    rate = soup.find(id=id).find("strong")

    return rate.text.strip().replace(',', '.')

class Currency:
    """
    Es utilizado para obtener los precios de las tasas de cambios proporcionados \
    por el Banco Central de Venezuela (BCV). https://www.bcv.org.ve/
    """
    def _load(self) -> None:
        response = _ensure_200_response('https://www.bcv.org.ve/')
        soup = BeautifulSoup(response.content, "html.parser")

        section_tipo_de_cambio_oficial = soup.find("div", "view-tipo-de-cambio-oficial-del-bcv")
        self.rates = {
            "EUR": _get_rate_by_id('euro', section_tipo_de_cambio_oficial),
            "CNY": _get_rate_by_id("yuan", section_tipo_de_cambio_oficial),
            "TRY": _get_rate_by_id("lira", section_tipo_de_cambio_oficial),
            "RUB": _get_rate_by_id("rublo", section_tipo_de_cambio_oficial),
            "USD": _get_rate_by_id("dolar", section_tipo_de_cambio_oficial)
        }
        self.rates['Fecha'] = _get_time(section_tipo_de_cambio_oficial)

    def get_rate(self, currency_code: str = None, prettify: bool = False) -> Union[dict[str, str], str]:
        """
        :currency_code: Especifica una tasa de cambio en especifico de obtener su valor. (`EUR`, `CNY`, `TRY`, `RUB`, `USD`, `Fecha`)
        :prettify: True si desea que el valor tenga el simbolo de la moneda en bolivares.
        """
        self._load()

        if not currency_code:
            return self.rates
        if currency_code not in self.rates:
            raise KeyError('Does not match any of the properties that were provided in the dictionary. Most information: https://github.com/fcoagz/pyBCV')
        
        if prettify and not currency_code == 'Fecha':
            return f'Bs. {self.rates[currency_code]}'
        return self.rates[currency_code]