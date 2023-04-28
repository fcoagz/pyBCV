 <p align="center">
 <img width="300" height="170" src="pyBCV/pybcv-preview.png">
</p>

# pyBCV
PyBCV es una librería desarrollada en el lenguaje de programación Python que se utiliza para recopilar los precios de los tipos de cambio y la tasas informativas del sistema bancario proporcionados por el Banco Central de Venezuela (BCV). Esta librería se centra específicamente en la obtención de los datos de tipos de cambio y las tasas informativas del BCV y los convierte en un formato fácilmente utilizable en Python.

## Instalación
Para instalar esta librería, puedes utilizar el siguiente comando:
```py
pip install pyBCV
```
Para actualizar esta librería, puedes utilizar el siguiente comando:
```py
pip install pyBCV --upgrade
```
## Uso
La clase `pyBCV.Currency` tiene los siguiente métodos:
- `refresh_period`: Inicializa la clase Currency con un período de actualización. Por defecto `timedelta = timedelta(hours=1)`.
- `lazy_load`: Indicador de carga. Matendra la tasa de cambio guardado en cache si vuelve a preguntar por la tasa nuevamente. por defecto `bool = False`.

El método `pyBCV.Currency().get_rate()` tiene los siguiente parametros:
- `currency_code`: Acepta un código de moneda o fecha como argumento.
- `prettify`: Acepta un valor booleano si desea que el valor de la moneda salga junto con el simbolo de Bolivares. `Bs. [VALOR]`
- `date_format`: Acepta un valor booleano si desea que la fecha extraiga la fecha y hora de la página web del Banco Central de Venezuela (BCV) o Formatea la fecha extraída en una cadena de texto legible. Por defecto `bool = True`. Extrae la fecha en una cadena de texto.

### Ejemplo:
```python
import pyBCV

bcv = pyBCV.Currency(lazy_load=True)

get_value_usd = bcv.get_rate(currency_code='USD')
get_in_bs_eur = bcv.get_rate(currency_code='EUR', prettify=True)
get_date_valid = bcv.get_rate(currency_code='Fecha', date_format=True)
```
Para obtener una estructura tipo JSON de las monedas disponibles en pyBCV, utilizamos la función `pyBCV.Currency().get_rate()` sin argumentos, el cual devuelve un diccionario.

La clase `pyBCV.Bank` tiene el siguiente método:
- `pyBCV.Bank().get_by_bank()`: Devuelve el sistema cambiario de compra y venta de moneda extranjera para un banco específico o todos los bancos disponibles.
### Ejemplo:
```python
import pyBCV

bcv = pyBCV.Bank()

get_bank = bcv.get_by_bank(bank_code='Banesco') # Devolvera un diccionario con los valores de compra y venta de moneda extranjera y su fecha valida.
specific_bank = bcv.get_by_bank(bank_code='Banesco', rate_or_sale='Compra') # Decolvera el valor de compra de moneda extranjera.
```

## Colaboradores

| [<img src="https://avatars.githubusercontent.com/u/103836660?v=4" width=115><br><sub>Francisco Griman</sub>](https://github.com/fcoagz) |  [<img src="https://avatars.githubusercontent.com/u/12820150?v=4" width=115><br><sub>Jesús Alfredo Reyes Vargas</sub>](https://github.com/jesusareyesv) |
| :---: | :---: |
## Propósito de pyBCV
El objetivo principal de PyBCV es proporcionar una forma fácil y rápida de acceder a los datos de tipos de cambio y tasas informativas del BCV en un formato que sea fácil de usar y manipular en Python. 