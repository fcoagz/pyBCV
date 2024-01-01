from bs4 import BeautifulSoup
from datetime import datetime

from ._requests import _ensure_200_response

class Bank:
    """
    La clase Bank se utiliza para obtener información sobre los tipos de cambio de compra y venta de moneda extranjera 
    para los bancos disponibles en el sistema bancario del Banco Central de Venezuela (BCV). 

    Atributos:
        start_date (datetime): Fecha de inicio para buscar los tipos de cambio.
        final_date (datetime): Fecha final para buscar los tipos de cambio.

    Ejemplo:
        ```python
        bank = Bank("01-01-2022", "31-12-2022")
        result = bank.get_by_bank("Banco de Venezuela")
        ```
    """
    def __init__(self, start_date: str, final_date: str = None) -> None:
        self.start_date = datetime.strptime(start_date, "%d-%m-%Y")
        if final_date:
            self.final_date = datetime.strptime(final_date, "%d-%m-%Y")
        else:
            self.final_date = datetime.now()
        self.result = []

    def _load(self):
        response = _ensure_200_response('https://www.bcv.org.ve/cambiaria/export/tasas-informativas-sistema-bancario')
        soup = BeautifulSoup(response.content, "html.parser")

        table_rows = soup.find_all('tr')
        data = {}

        for row in table_rows:
            values = row.find_all('td') 
            
            if len(values) > 3:
                fecha_str = values[0].text.strip()
                rate = {
                    "bank": values[1].text.strip(),
                    "compra": values[2].text.strip().replace(',', '.'),
                    "venta": values[3].text.strip().replace(',', '.')
                }
                if not data.get(fecha_str, None):
                    data[fecha_str] = []
                data[fecha_str].append(rate)

        for fecha_str in data:
            fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
            if self.start_date <= fecha <= self.final_date:
                self.result.append({fecha_str: data[fecha_str]})
    
    def get_by_bank(self, bank_code: str = None):
        """
        Devuelve los tipos de cambio para un banco específico.
        """
        self._load()

        if not bank_code:
            return self.result

        result_dict = {}
        for result in self.result:
            for fecha_str, rates in result.items():
                for rate in rates:
                    if bank_code == rate['bank']:
                        if fecha_str not in result_dict:
                            result_dict[fecha_str] = []
                        result_dict[fecha_str].append(rate)

        if not result_dict:
            raise KeyError(f"Bank code {bank_code} does not match any of the properties that were provided. For more information, visit: https://github.com/fcoagz/pyBCV")

        return result_dict