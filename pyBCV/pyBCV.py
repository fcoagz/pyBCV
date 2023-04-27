import locale
from decimal import Decimal
from typing import Any, Callable
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from .core.requests import BCVRequests

def _extract_timestamp(soup: BeautifulSoup) -> datetime:
    try:
        return datetime.fromisoformat(
            soup.find("span", "date-display-single").get("content")
        )
    except:
        return None

def _formatted_date(soup: BeautifulSoup) -> str:
    locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
    current_date = _extract_timestamp(soup)
    day_weekday = current_date.weekday()

    day_name = (
        'Lunes' if day_weekday == 0 else
        'Martes' if day_weekday == 1 else
        'Miercoles' if day_weekday == 2 else
        'Jueves' if day_weekday == 3 else
        'Viernes'
    )

    if current_date is not None:
        return current_date.strftime(f'{day_name}, %d %B del %Y')

def _get_rate_by_id(tag_id: str, soup: BeautifulSoup) -> Decimal:
    try:
        rate_value = soup.find(id=tag_id).find("strong").text.strip().replace(",", ".")
        rate_value = Decimal(rate_value)
    except:
        rate_value = None

    return rate_value


class Currency:
    """
    `pyBCV.Currency()`. Es la instancia principal para obtener los datos de tipo de cambio del BCV.\n
    https://github.com/fcoagz/pyBCV#uso

    ```py
    import pyBCV

    bcv = pyBCV.Currency()
    bcv.get_rate(currency_code='USD')
    ```
    """

    def __init__(
        self,
        refresh_period: timedelta = timedelta(hours=1),
        lazy_load: bool = False,
    ):
        self.refresh_period = refresh_period
        self.rates = {}
        self.loaded = False
        self.last_request_timestamp = None
        self.lazy_load = lazy_load
        if not self.lazy_load:
            self._load()

    def _load(self):
        self.loaded = False
        if (
            self.last_request_timestamp
            and (datetime.now() - self.last_request_timestamp) < self.refresh_period
        ):
            return

        soup = BeautifulSoup(BCVRequests.get_main_page(), "html.parser")
        section_tipo_de_cambio_oficial = soup.find(
            "div", "view-tipo-de-cambio-oficial-del-bcv"
        )

        self.rates = {
            "EUR": _get_rate_by_id("euro", section_tipo_de_cambio_oficial),
            "CNY": _get_rate_by_id("yuan", section_tipo_de_cambio_oficial),
            "TRY": _get_rate_by_id("lira", section_tipo_de_cambio_oficial),
            "RUB": _get_rate_by_id("rublo", section_tipo_de_cambio_oficial),
            "USD": _get_rate_by_id("dolar", section_tipo_de_cambio_oficial),
            "Fecha": [_extract_timestamp(section_tipo_de_cambio_oficial), _formatted_date(section_tipo_de_cambio_oficial)]
        }
        self.loaded = True
        self.last_request_timestamp = datetime.now()

    def _pretty_rates(self) -> dict[str, str]:
        return {
            k: (f"Bs {value}" if k != "Fecha" else value.isoformat())
            for k, value in self.rates.items()
        }

    def get_rate(
        self, currency_code: str = None, prettify: bool = False, date_format: bool = True
    ) -> dict[str, str] | str | dict[str, float] | float:
        """
        El módulo `get_rate()` acepta un código de moneda como argumento y devuelve
        la tasa de cambio actual de esa moneda.
        """

        if (
            not self.last_request_timestamp
            or (datetime.now() - self.last_request_timestamp) >= self.refresh_period
        ):
            self._load()

        if currency_code == 'Fecha':
            return self.rates[currency_code][0] if not date_format else self.rates[currency_code][1]

        if not currency_code:
            return self.rates if not prettify else self._pretty_rates()

        return (
            self.rates[currency_code]
            if not prettify
            else f"Bs. {self.rates[currency_code]}"
        )


class Bank:
    """
    `pyBCV.Bank()`. Es la segunda instancia para obtener los datos del sistema bancario del BCV.\n
    https://github.com/fcoagz/pyBCV#uso

    ```py
    import pyBCV

    bcv = pyBCV.Bank()
    bcv.get_by_bank(bank_code='Banesco', rate_or_sale='Compra')
    ```
    """

    def get_by_bank(
        self, bank_code=None, rate_or_sale=None
    ) -> dict[Any, dict[str, str]] | str | dict[str, str]:
        """
        El módulo `get_by_bank()` acepta el nombre de un banco como argumento y devuelve la fecha vigente y el sistema cambiario de compra y venta de moneda extranjera para ese banco.
        """

        soup = BeautifulSoup(BCVRequests.get_tasas_bancos(), "html.parser")

        date_indicator = []
        title_bank = []
        rate_buys = []
        rate_sales = []

        for i in soup.find_all(
            "td", "views-field views-field-field-fecha-del-indicador"
        ):
            date_indicator.append(i.text.strip())
        for j in soup.find_all("td", "views-field views-field-views-conditional"):
            title_bank.append(j.text.strip())
        for k in soup.find_all("td", "views-field views-field-field-tasa-compra"):
            rate_buys.append(k.text.strip().replace(",", "."))
        for e in soup.find_all("td", "views-field views-field-field-tasa-venta"):
            rate_sales.append(e.text.strip().replace(",", "."))

        bank = {
            title_bank[0]: {
                "Fecha": date_indicator[0],
                "Compra": f"Bs. {rate_buys[0]}",
                "Venta": f"Bs. {rate_sales[0]}",
            },
            title_bank[1]: {
                "Fecha": date_indicator[1],
                "Compra": f"Bs. {rate_buys[1]}",
                "Venta": f"Bs. {rate_sales[1]}",
            },
            title_bank[2]: {
                "Fecha": date_indicator[2],
                "Compra": f"Bs. {rate_buys[2]}",
                "Venta": f"Bs. {rate_sales[2]}",
            },
            title_bank[3]: {
                "Fecha": date_indicator[2],
                "Compra": f"Bs. {rate_buys[2]}",
                "Venta": f"Bs. {rate_sales[3]}",
            },
        }

        if not bank_code:
            return bank

        elif rate_or_sale in bank[bank_code]:
            return bank[bank_code][rate_or_sale]

        elif bank_code in bank:
            return bank[bank_code]