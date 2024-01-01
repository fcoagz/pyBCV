<p align="center">
 <img width="300" height="170" src="https://github.com/fcoagz/pyBCV/blob/main/pyBCV/pybcv-preview.png?raw=true">
</p>

# pyBCV
pyBCV es una librería de Python que simplifica la obtención de los precios de los tipos de cambio y las tasas informativas del sistema bancario proporcionados por el Banco Central de Venezuela (BCV) convirtiéndolos en un formato fácilmente utilizable en Python.

## Instalación
Para instalar esta librería, puedes utilizar el siguiente comando:
```py
pip install pyBCV
```
## Uso
La librería pyBCV proporciona dos clases, `Currency` y `Bank`, para obtener tasas de cambio e informativas de bancos del Banco Central de Venezuela.

La clase `Currency` obtiene tasas de cambio para varias monedas y las devuelve en formato de diccionario. También proporciona métodos para obtener una tasa de cambio específica o la hora de la última actualización.
```py
from pyBCV import Currency

currency = Currency()
all_rates = currency.get_rate() # obtener todas las tasas de cambio de moneda
usd_rate = currency.get_rate(currency_code='USD', prettify=False) # obtener la tasa de cambio del dólar estadounidense sin símbolo de moneda
last_update = currency.get_rate(currency_code='Fecha') # obtener la hora de la última actualización
```

La clase Bank obtiene tasas informativas proporcionadas por varios bancos en Venezuela y las devuelve en formato de lista de diccionarios. Proporciona métodos para obtener información sobre un banco específico o todos los bancos disponibles.
```py
from pyBCV import Bank

bcv = Bank("01-01-2023", "31-12-2023") # Inicializar la clase Bank con fechas de inicio y final
bank_info = bcv.get_by_bank() # Obtener todas las tasas de cambio informativas de los bancos disponibles

# Obtener la tasa de cambio informativa del Banco Nacional de Crédito
bnc_info = bcv.get_by_bank(bank_code='Banco Nacional de Crédito') 

```
## Colaboradores

| [<img src="https://avatars.githubusercontent.com/u/103836660?v=4" width=115><br><sub>Francisco Griman</sub>](https://github.com/fcoagz) |  [<img src="https://avatars.githubusercontent.com/u/12820150?v=4" width=115><br><sub>Jesús Alfredo Reyes Vargas</sub>](https://github.com/jesusareyesv) |
| :---: | :---: |
## Propósito de pyBCV
Esta librería está diseñada específicamente para recopilar y convertir estos datos en un formato fácilmente utilizable en Python, lo que permite a los desarrolladores acceder a ellos y utilizarlos en sus aplicaciones con facilidad. Con pyBCV, los usuarios pueden obtener información actualizada sobre las tasas de cambio y las tasas informativas de los bancos de manera rápida y sencilla, haciendo que el proceso de obtener estos datos sea más eficiente y conveniente.