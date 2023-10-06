"""CASO 3 BA: OPTIMIZACIÓN ECOMMERCE
En este caso trabajaremos como consultores para un ecommerce del sector cosméticos.

Esta empresa ha teniendo una evolución plana durante los últimos meses y nos ha contratado para analizar sus datos transaccionales e implementar acciones CRO personalizadas a su situación en base a dicho análisis.

En este caso entre otras cosas vamos a aprender:

- cómo son los datos de un ecommerce
- técnicas de análisis orientadas a incrementar facturación y margen en un ecommerce, tanto básicas o genéricas como algunas técnicas avanzadas específicas de este sector
- las principales métricas sobre las que tenemos que trabajar y algunas acciones CRO que podemos poner en práctica para mejorarlas
- a construir dos recursos analíticos muy potentes para este sector: una segmentación RFM y un sistema de recomendación.

Por tanto, mucho de lo que aprendamos aquí es de aplicación general en prácticamente cualquier ecommerce.

Siguiendo la metodología de Discovery:

OBJETIVO

Analizar los datos transaccionales para intentar potenciales acciones CRO que incrementen visitas, conversiones y ticket medio, y por tanto incrementar la facturación global del ecommerce.

Crear activos analíticos avanzados como una segmentación RFM y un sistema de recomendación que impulsen la consecución del objetivo.

PALANCAS

Como siempre vamos a entender primero el negocio, y sus principales procesos, métricas y conceptos.

Fuente del gráfico: https://en.wikipedia.org/wiki/File:Wikipedia_Mobile_User_Journey.pdf

from IPython import display
display.Image("../../../99_Media/customerjourney.png")

El primer paso es cuando un usuario llega a la web del ecommerce. Normalmente vendrá desde:

- Campañas de pago: paid ads como Facebook Ads o Google Ads
- Contenido orgánico: blog, rrss, ...
- Tráfico directo: conoce la url y la introduce en el navegador

Ese tráfico se llama visitas, y las páginas que van viendo se llaman páginas vistas, aunque en nuestro caso lo llamaremos views.

El usuario navega por la web y cuando le gusta un producto lo mete en el carrito.

Finalmente puede sacar productos del carrito, salir sin comprar nada, o finalmente hacer el pedido.

Un proceso común es la venta cruzada, en la cual se recomiendan al usuario otros productos que también podrían interesarle.

Incluso cuando se ha ido podemos volver a contartar al usuario mediante retargeting o email marketing.

Todo este proceso se llama funnel o también customer journey.

En el entorno online prácticamente todo se puede registrar.

El registro del usuario puede ser logado o no.

La secuencia de acciones que hace un usuario en la misma sesión de navegación se llama sesión.

El ratio de compras sobre las visitas se llama ratio de conversión.

Además existen otras métricas clave que tenemos que dominar para gestionar correctamente un ecommerce:

- CPA. Coste por Adquisición. ¿Cuánto nos cuesta obtener un nuevo cliente? Idea que CPA > LTV
- AOV. Average Order Value. Ticket medio de la compra del cliente
- Frecuencia de compra. Cuantas veces más compra el cliente
- LTV. Life Time Value. El valor del cliente en el tiempo. AOV son todas las compras que hace el cliente, p.e. en un año.
- Churn. Pago recurrente, p.e. SaaS. Esto mide, de cada 100 clientes inicialmente, cuantos se van cayendo.

CONCEPTO CLAVE: Solo existen 3 formas de incrementar un negocio:

- Más clientes: esto implica conseguir más visitas y mayor conversión
- Más frecuencia: esto implica conseguir que los mismos clientes compren más veces
- Mayor ticket medio: esto implica conseguir que se compre más o más caro en la misma sesión de compra

Para conseguir esos 3 efectos trabajamos sobre las siguientes palancas operativas:

- Customer journey: cómo podemos optimizar cada uno de los pasos del proceso
- Clientes: cómo podemos usar la info disponible de los clientes para optimizar las campañas que realicemos
- Productos: cómo podemos optimizar el catálogo de productos e identificar de manera personalizada qué productos tenemos que poner delante de cada cliente

Entenderemos en nuestro caso CRO de manera amplia, es decir como la disciplina que pone en práctica acciones para trabajar sobre las palancas y conceptos anteriores.

KPIs

- Visitas
- Conversión
- Frecuencia de compra
- Ticket medio
- Tasa abandono carrito
- LTV

ENTIDADES Y DATOS

En nuestro caso las entidades que tenemos en la granularidad de los datos son:

- Usuarios
- Clientes
- Sesiones
- Eventos
- Productos

PREGUNTAS SEMILLA

Habiendo entendido las palancas, KPIs y entidades ya podemos plantear las preguntas semilla:

Sobre el customer journey:

- ¿Cómo es un proceso típico de compra?
- ¿Cuántos productos se ven, se añaden al carro, se abandonan y se compran de media en cada sesión?
- ¿Cómo ha sido la tendencia de estos indicadores en los últimos meses?

Sobre los clientes:

- ¿Cuántos productos compra cada cliente?
- ¿Cuánto se gasta cada cliente?
- ¿Hay "mejores clientes" que haya que identificar y tratar de forma diferente?
- ¿Los clientes repiten compras en los siguientes meses?
- ¿Cual es el LTV medio de un cliente?
- ¿Podemos diseñar campañas personalizas al valor del cliente?

Sobre los productos:

- ¿Cuales son los productos más vendidos?
- ¿Hay productos que no se venden?
- ¿Existe relación entre el precio del producto y su volumen de ventas?
- ¿Hay productos que se visiten pero no se compren?
- ¿Hay productos que se saquen recurrentemente del carrito?
- ¿Se podrían hacer recomendaciones personalizadas de productos para cada cliente?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %matplotlib inline # para que los gráficos aparezcan en Jupyter Notebook
# %config IPCompleter.greedy=True # cuando pulsamos la tecla tabuladora que autocomplete

# Formato de display
pd.options.display.float_format = '{:15.2f}'.format

# ENTENDER LOS FICHEROS

import sqlalchemy as sa
con = sa.create_engine('sqlite:///DatosEcommerce/ecommerce.db')

from sqlalchemy import inspect
insp = inspect(con)
tablas = insp.get_table_names()
print(tablas)

oct = pd.read_sql('2019-Oct', con)
nov = pd.read_sql('2019-Nov', con)
dic = pd.read_sql('2019-Dec', con)
ene = pd.read_sql('2020-Jan', con)
feb = pd.read_sql('2020-Feb', con)

# INTEGRACION DE DATOS

df = pd.concat([oct,nov,dic,ene,feb], axis = 0)
print(df)

# CALIDAD DE LOS DATOS

df.info()

# Eliminamos la columna index.

df.drop(columns = 'index', inplace = True)

# Análisis y corrección de tipos.

# - pasar event_time a datetime
# Pasamos event_time a datetime.

# TRUCO PRO: pd.to_datetime() puede tardar mucho en ejecutarse en datasets grandes.
# Pero por algún motivo si dividimos la cadena de la fecha en sus partes y la volvemos a juntar y después transformamos a datetime especificándole el formato exacto funciona MUCHO más rápido.

# Te voy a enseñar las dos formas:

# - la fácil y tradicional con pd.to_datetime: puedes usar esta si no quieres complicarte con la función
# la avanzada creando una función para hacer lo que he comentado

# Te recuerdo el link para los códigos de los formatos:
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

# En mi equipo con 32GB de RAM la forma tradicional tardó más de 5 minutos, mientras que la avanzanda menos de 10 segundos.

#forma tradicional, la dejo comentada porque voy a utilizar la otra
#df.event_time = pd.to_datetime(df.event_time)

# forma avanzada crando una función
# A esta función hay que pasarle la variable fecha y el formato en el que está:

def datetime_rapido(dt,formato):

    def divide_fecha(fecha):
        division = fecha.split()
        date = division[0]
        time = division[1]
        cadena = date + ' ' + time
        return cadena

    resultado = pd.to_datetime(dt.apply(lambda x: divide_fecha(x)), format = formato)

    return resultado

formato = '%Y-%m-%d %H:%M:%S'
df.event_time = datetime_rapido(df.event_time,formato)

df.info()

# Nombres de variables. Renombramos las variables a español.

df.columns = ['fecha',
              'evento',
              'producto',
              'categoria',
              'categoria_cod',
              'marca',
              'precio',
              'usuario',
              'sesion']

# Análisis de nulos

print(df.isna().sum().sort_values(ascending = False))

# CONCLUSIONES:

# - categoria_cod tiene casi todos los registros a nulo
# - marca tiene casi la mitad de los registros a nulo
# - hay 500 nulos en sesión

# Acciones:

# - eliminar las variables categoria_cod y marca
# - eliminar los nulos de sesión ya que es una variable relevante

df = df.drop(columns = ['categoria_cod','marca']).dropna()

# Análisis de las variables numéricas

print(df.describe().T)

# Vemos negativos en el precio. Vamos a profundizar.

print(df[df.precio <= 0])

# Son unos 20000 registros, podríamos eliminarlos.
# Pero antes ¿se concentran quizá en algún producto determinado?

print(df[df.precio <= 0].producto.value_counts().head(10))

# No parece que sea problema de un producto concreto, así que vamos a eliminar todos los registros.

df = df[df.precio > 0]

# Análisis de las variables categóricas

print(df.evento.nunique())
print(df.evento.value_counts())

print(df.producto.nunique())
print(df.categoria.nunique())

# Índice

df.set_index('fecha', inplace = True)

# TRANSFORMACIÓN DE DATOS

# Vamos a crear 3 tipos de nuevas variables

# - Extraer componentes
# - Variables de calendario: Festivos locales (Rusia)
# - Indicadores exógenos: Días no necesariamente festivos pero con interés comercial: Black Friday, Cyber Monday, Reyes, San Valentin

def componentes_fecha(dataframe):
    date = dataframe.index.date
    año = dataframe.index.year
    mes = dataframe.index.month
    dia = dataframe.index.day
    hora = dataframe.index.hour
    minuto = dataframe.index.minute
    segundo = dataframe.index.second
    
    
    return(pd.DataFrame({'date':date, 'año':año,'mes':mes, 'dia':dia, 'hora':hora, 'minuto':minuto, 'segundo':segundo}))


print(df)

df = pd.concat([df.reset_index(),componentes_fecha(df)], axis = 1).set_index('fecha')

print(df)

# Variables de calendario: festivos
# Para incorporar festivos podemos usar el paquete holidays.

# No es perfecto, pero nos da mucha flexibilidad porque tiene fiestas de varios países e incluso a nivel comunidades.
# Lo instalamos con: conda install -c conda-forge holidays

# Lo importamos con: import holidays
# Y podemos ver el listado de países y el uso básico en:
# https://github.com/dr-prodigy/python-holidays

# Por ejemplo vamos a hacer la prueba con España.

import holidays

festivo_es = holidays.ES(years=2021)

for fecha, fiesta in festivo_es.items():
    print(fecha,fiesta)

# Definimos el objeto festivo_ru ya que este ecommerce es Ruso.

festivo_ru = holidays.RU(years=2020)

# Vamos a incorporar una variable que diga en cada registro si era un día festivo o no.

df['festivo'] = df.date.apply(lambda x: 1 if (x in festivo_ru) else 0)

# Comprobamos los festivos:

print(df[df.festivo == 1].date.value_counts().sort_index())

# Indicadores exógenos

# Vamos a añadir indicadores para Black Friday y San Valentín.

df['black_friday'] = 0
df.loc['2019-11-29','black_friday'] = 1

df['san_valentin'] = 0
df.loc['2020-02-14','san_valentin'] = 1

print(df['black_friday'].value_counts())
print(df['san_valentin'].value_counts())

# TABLON ANALITICO FINAL

print(df.head())

# Vamos a poner las columnas en un orden más natural.

variables = df.columns.to_list()

orden = ['usuario',
         'sesion',
         'categoria',
         'evento',
         'producto',
         'precio']

resto = [nombre for nombre in variables if nombre not in orden]

df = df[orden + resto]

# Guardamos como pickle para no perder los metadatos.

df.to_pickle('DatosEcommerce/tablon_analitico.pickle')
