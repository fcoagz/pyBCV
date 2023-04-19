 <p align="center">
 <img width="300" height="170" src="pyBCV/pybcv-preview.png">
</p>

# pyBCV
PyBCV es una librería desarrollada en el lenguaje de programación Python que se utiliza para recopilar los precios de los tipos de cambio y la tasas informativas del sistema bancario proporcionados por el Banco Central de Venezuela (BCV). Esta librería se centra específicamente en la obtención de los datos de tipos de cambio y las tasas informativas del BCV y los convierte en un formato fácilmente utilizable en Python.

## Instalación
Para instalar esta librería, puedes utilizar el siguiente comando de pip:
```py
pip install --upgrade pyBCV
```
Si usas un Sistema Operativo como Linux o Mac:
```py
pip3 install --upgrade pyBCV
```

## Uso
Para obtener información del BCV, creamos una instancia de la clase `Currency` o `Bank` y elegimos el módulo que deseamos utilizar para obtener la información. En pyBCV, los módulos disponibles son:

- Currency().get_rate(): Obtiene la tasa de cambio actual de una moneda específica.
- Bank().get_by_bank(): Obtiene la fecha vigente y el sistema cambiario de compra y venta de moneda extranjera para un banco específico.

A continuación te digo como se utiliza estos módulos:
### Módulo **get_rate()**
___
El módulo `get_rate()` acepta un código de moneda como argumento y devuelve la tasa de cambio actual de esa moneda.
```py
import pyBCV

bcv = pyBCV.Currency()

tasa_usd = bcv.get_rate('USD')
print(tasa_usd)

>> 'Bs. 24.56330000'
```
Para obtener una estructura tipo JSON de las monedas disponibles en pyBCV, utilizamos el módulo get_rate() sin argumentos, el cual devuelve un diccionario.
```py
import pyBCV

bcv = pyBCV.Currency()

tasa_de_cambio = bcv.get_rate()
print(tasa_de_cambio)

>> {'EUR': 'Bs. 26.92555256', 'CNY': 'Bs. 3.57247989', 'TRY': 'Bs. 1.26605811', 'RUB': 'Bs. 0.30064870', 'USD': 'Bs. 24.56330000'}
```

### Módulo **get_by_bank()**
___
El módulo `get_by_bank()` acepta el nombre de un banco como argumento y devuelve la fecha vigente y el sistema cambiario de compra y venta de moneda extranjera para ese banco.
```py
import pyBCV

bcv = pyBCV.Bank()

banco = bcv.get_by_bank('Bancamiga')
print(banco)

>> {'Fecha': '18-04-2023', 'Compra': 'Bs. 24.5275', 'Venta': 
'Bs. 24.5991'}
``` 
Para acceder a una sola propiedad. El módulo `get_by_bank()` acepta el nombre de un banco como primer argumento y el nombre de una propiedad como segundo argumento (por ejemplo: "Fecha") y devuelve el valor de esa propiedad para el banco especificado.
```py
import pyBCV

bcv = pyBCV.Bank()

banco = bcv.get_by_bank('Bancamiga', 'Fecha')
print(banco)

>> '18-04-2023'
``` 
Si queremos obtener una estructura tipo JSON de los bancos disponibles en pyBCV, utilizamos el módulo `get_by_bank()` sin argumentos.
```py
import pyBCV

bcv = pyBCV.Bank()

bancos = bcv.get_by_bank()
print(bancos)

>> {'Banco Nacional de Crédito BNC': {'Fecha': '18-04-2023', 'Compra': 'Bs. 24.3989', 'Venta': 'Bs. 24.4180'}, 'Bancamiga': {'Fecha': '18-04-2023', 'Compra': 'Bs. 24.5275', 'Venta': 
'Bs. 24.5991'}, 'Banesco': {'Fecha': '18-04-2023', 'Compra': 'Bs. 24.5685', 'Venta': 'Bs. 24.6619'}, 'BBVA Provincial': {'Fecha': '18-04-2023', 'Compra': 'Bs. 24.5685', 'Venta': 'Bs. 24.6770'}}
``` 
# Propósito de pyBCV
El objetivo principal de PyBCV es proporcionar una forma fácil y rápida de acceder a los datos de tipos de cambio y tasas informativas del BCV en un formato que sea fácil de usar y manipular en Python. 