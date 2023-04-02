# pyBCV
PyBCV es una librería desarrollada en el lenguaje de programación Python que se utiliza para recopilar los precios de los tipos de cambio proporcionados por el Banco Central de Venezuela (BCV). Esta librería se centra específicamente en la obtención de los datos de tipos de cambio del BCV y los convierte en un formato fácilmente utilizable en Python.

## Instalación
Para instalar esta librería, puedes utilizar el siguiente comando de pip:
```py
pip install pyBCV
```
Si usas un Sistema Operativo como Linux o Mac:
```py
pip3 install pyBCV
```

## Uso
1. Importamos la librería:
```py
import pyBCV
```
2. Creamos una instancia de la clase `Currency`. y asignamos el módulo `get_rate()` a nuestra instancia `bcv` para obtener el tipo de cambio actual imprimiendo en consola:
```py
import pyBCV

bcv = pyBCV.Currency()

print(bcv.get_rate())

>> {'EUR': 'Bs. 26.65', 'CNY': 'Bs. 3.57', 'TRY': 'Bs. 1.28', 'RUB': 'Bs. 0.32', 'USD': 'Bs. 24.53'}
```
Retorna una estructura JSON.

3. Puedes proporcionarle un parametro al módulo `get_rate()` para obtener el tipo de cambio actual de una moneda:
```py
import pyBCV

bcv = pyBCV.Currency()

print(bcv.get_rate('USD'))

>> 'Bs. 24.53'
```