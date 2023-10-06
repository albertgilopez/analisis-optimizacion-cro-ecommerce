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

df = pd.read_pickle('tablon_analitico.pickle')
print(df)

# CUSTOMER JOURNEY

# ¿Cómo está funcionndo el Customer Journey?

eventos = df.evento.value_counts()
print(eventos)

"""kpi_visualizaciones_p = 100
kpi_carrito_p = eventos.loc['cart'] / eventos.loc['view'] * 100
kpi_abandono_p = eventos.loc['remove_from_cart'] / eventos.loc['cart'] * 100
kpi_compra_p = eventos.loc['purchase'] / eventos.loc['cart'] * 100

kpis = pd.DataFrame({'kpi':['visitas','carrito','abandono','compra'],
                     'valor':[kpi_visualizaciones_p,kpi_carrito_p,kpi_abandono_p, kpi_compra_p]})

print(kpis)"""

kpi_visualizaciones_p = 100
kpi_carrito_p = eventos.loc['cart'] / eventos.loc['view'] * 100
kpi_abandono_p = eventos.loc['remove_from_cart'] / eventos.loc['cart'] * 100
kpi_compra_p = eventos.loc['purchase'] / eventos.loc['cart'] * 100

kpis = pd.DataFrame({'kpi':['visitas','carrito','compra'],
                     'valor':[kpi_visualizaciones_p,kpi_carrito_p,kpi_compra_p]})

print(kpis)

from plotly import graph_objects as go

fig = go.Figure(go.Funnel(
    y = kpis.kpi,
    x = kpis.valor.round(2),
    marker = {'color': ['red','blue','green']},
    opacity = 0.3
    ))

fig.update_layout(
    title = 'Funnel Conversión Inicial')
    
# fig.show()

# CONCLUSIONES

# Las tasas de partida son un 60% de carrito sobre visualiazaciones y un 22% de compra sobre carrito
# Por tanto existe un 40% de visitas sobre las que hay que trabajar para conseguir más carritos, y un 78% de carritos sobre los que trabajar para conseguir más compras

# TRUCO PRO:

# Este tipo de análisis conviene encapsularlo en funciones.
# De tal forma que ante un nuevo cliente que tenga la misma estructura de datos podremos preparar informes automáticos para los análisis más frecuentes.
# Por ejemplo vamos a crear una función para hacer funnel analytics.

# Esta función recibe la variable de los eventos como entrada
def funnel_analytics(evento):
    
    # Hacemos el conteo de eventos
    eventos = df.evento.value_counts()

    # Preparamos las variables
    kpi_visitas_p = 100
    kpi_carrito_p = eventos.loc['cart'] / eventos.loc['view'] * 100
    kpi_abandono_p = eventos.loc['remove_from_cart'] / eventos.loc['cart'] * 100
    kpi_compra_p = eventos.loc['purchase'] / eventos.loc['cart'] * 100
    kpis = pd.DataFrame({'kpi':['visitas','carrito','compra'],
                         'valor':[kpi_visitas_p,kpi_carrito_p,kpi_compra_p]})
    
    # Creamos el gráfico
    from plotly import graph_objects as go
    fig = go.Figure(go.Funnel(
        y = kpis.kpi,
        x = kpis.valor.round(2),
        marker = {'color': ['red','blue','green']},
        opacity = 0.3
        ))

    fig.update_layout(
        title = 'Funnel Conversión Inicial')

    fig.show()
    
    # Imprimimos un informe de conclusiones
    print(f'Las tasas de partida son un {kpi_carrito_p.round(2)}% de carrito sobre visualiazaciones y un {kpi_compra_p.round(2)}% de compra sobre carrito. \n')
    print(f'Por tanto existe un {100 - kpi_carrito_p.round(2)}% de visitas sobre las que hay que trabajar para conseguir más carritos, y un {100 - kpi_compra_p.round(2)}% de carritos sobre los que trabajar para conseguir más compras.')

# funnel_analytics(df.evento)

# ¿Cuántos productos se ven, se añaden al carro, se abandonan y se compran de media en cada sesión?

# A diferencia del análisis macro del funnel este análisis es por sesión, lo cual lo hace más operativo.
# Conocer los principales KPIs por sesión nos permite establecer la línea base para ir midiendo los resultados de las acciones de CRO.
# Primero creamos un dataframe con la granularidad a nivel de sesión y evento que necesitamos.

sesion_prod = df.groupby(['sesion','evento']).producto.count()
print(sesion_prod)

# Pasamos los eventos a columnas

sesion_prod = sesion_prod.unstack().fillna(0)
print(sesion_prod)

# Para comprobar calculamos los totales y debería darnos los mismos que a nivel global.

print(sesion_prod.sum())

# Reordenamos las columnas

sesion_prod = sesion_prod[['view','cart','remove_from_cart','purchase']]
print(sesion_prod)

# Calculamos la media de cada evento por sesión.

media_eventos_sesion = sesion_prod.mean()
print(media_eventos_sesion)

# CONCLUSIÓN:

# En cada sesión, de media:

# - Se ven 2.2 productos
# - Se añaden 1.3 productos al carrito
# - Se eliminan 0.9 productos del carrito
# - Se compran 0.3 productos

# Como decíamos, éstos son los números que deberemos incrementar con las acciones de CRO.

# ¿Existen diferencias entre los eventos por horas?

# Creamos el dataframe a granularidad evento y hora.

eventos_hora = df.groupby(['evento','hora']).producto.count()
print(eventos_hora)

# Pasamos los eventos a columnas.

eventos_hora = eventos_hora.unstack(level = 0)
print(eventos_hora)

# Vamos a visualizar cómo se distribuyen los eventos por hora.

eventos_hora.plot()
plt.xticks(ticks = eventos_hora.index);

# Existe una pauta global como era de esperar.
# Pero para ver mejor las diferencias podemos crear una nueva variable que sea el ratio de compras por visita en cada hora.

eventos_hora['compras_visitas'] = eventos_hora.purchase / eventos_hora.view * 100
print(eventos_hora)

# Reordenamos las variables

eventos_hora = eventos_hora[['view','cart','remove_from_cart','purchase','compras_visitas']]
print(eventos_hora)

# Visualizamos para ver si hay horas en las que se compra proporcionalmente más.

plt.figure(figsize = (12,6))
sns.lineplot(data = eventos_hora, x = eventos_hora.index, y = 'compras_visitas')
plt.xticks(eventos_hora.index);

# CONCLUSIONES:

# - Las horas en las que la gente compra más son la 1, las 8, de 11 a 13 y las 18
# - Las horas en las que la gente no compra son las 24, de 3 a 7, de 14 a 17 y de 19 a 23

# Vamos a analizar ahora no de forma proporcional, si no en absoluto si existen o no horas más frecuentes para cada tipo de evento.

plt.figure(figsize = (12,12))
sns.heatmap(data = eventos_hora);

# El problema es que como cada evento tiene diferente escala este gráfico no nos permite diferenciar bien los patrones.
# Para solucionarlo podemos usar la tipificación de variables que aprendimos en el módulo de estadística.

def tipificar(variable):
    media = variable.mean()
    dt = variable.std()
    return(variable.apply(lambda x: (x - media) / dt))

eventos_hora_tip = eventos_hora.apply(tipificar)
print(eventos_hora_tip)

plt.figure(figsize = (12,12))
sns.heatmap(data = eventos_hora_tip);

# Vamos a sacar también los gráficos de líneas para verlo más claramente.

eventos_hora_tip.plot(subplots = True, sharex = False, figsize = (12,12),xticks = eventos_hora_tip.index);

# INSIGHT #1: Todas las métricas se maximzan en las franjas entre las 9 y las 13 y entre las 18 y las 20

# - Esta info es muy relevante por ejemplo de cara a paid ads, tanto de generación de tráfico como de retargeting
# - Además, parece haber algún subtipo de usuario que compra a la 1 de la mañana, que aunque no sea muy frecuente sí compra mucho

# ¿Cuál es la media de facturación mensual?

print(df.loc[df.evento == 'purchase'].groupby('mes').precio.sum().mean())

# ¿Cuál es la tendencia de los úlimos meses?

tendencia = df.groupby('evento').resample('W').evento.count().unstack(level = 0)
tendencia = tendencia[['view','cart','remove_from_cart','purchase']]
print(tendencia)

tendencia.plot(subplots = True, figsize = (12,6), sharex = True, xticks = tendencia.index, x_compat=True, rot = 90);

# La tendencia es plana en todas las métricas, lo que confirma la necesidad de las acciones de CRO.
# Existe un pico significativo en la semana del 24, obviamente por black friday, vamos a hacer el mismo análisis pero diario y solo para noviembre y dicienbre para ver el efecto.

tendencia_diaria = df.loc['2019-11':'2019-12'].groupby('evento').resample('D').evento.count().unstack(level = 0)
tendencia_diaria = tendencia_diaria[['view','cart','remove_from_cart','purchase']]
print(tendencia_diaria)

tendencia_diaria.plot(subplots = True, figsize = (16,10), sharex = True, xticks = tendencia_diaria.index, x_compat=True, rot = 90);

# CONCLUSIONES:

# - Efectivamente el pico coincide con el black friday (día 29)
# - Pero aún hay un pico mayor unos días antes, el día 22, posiblemente por el inicio de la semana black friday
# - Sorprendemente los propios días de Navidad tienen una tendencia decreciente, lo que significa que los consumidores claramente han adelantado sus compras
# - Vamos a hacer el mismo análisis para Enero y Febrero.

tendencia_diaria = df.loc['2020-01':'2020-02'].groupby('evento').resample('D').evento.count().unstack(level = 0)
tendencia_diaria = tendencia_diaria[['view','cart','remove_from_cart','purchase']]
tendencia_diaria.plot(subplots = True, figsize = (16,10), sharex = True, xticks = tendencia_diaria.index, x_compat=True, rot = 90);

# CONCLUSIONES:

# - Durante la semana de Reyes tampoco hay pico de ventas
# - Ni los días previos a San Valentín
# - Pero sí hay un pico muy pronunciado el 27 de Enero, seguramente algún evento local

# INSIGHT #2 La gran conclusión es que todo el pastel de las compras navideñas se reparte en la semana del black friday

# ¿Momentos de la verdad?

# ¿Podríamos llegar a identificar momentos a nivel de día-hora en los que se producen el mayor número de compras?
# Sería muy útil para concentrar gran parte de la inversión de campañas justo en esos momentos.

compras_dia_hora = df.loc[df.evento == 'purchase'].groupby(['date','hora']).evento.count().unstack(level = 0).fillna(0)
print(compras_dia_hora)

plt.figure(figsize = (20,14))
sns.heatmap(compras_dia_hora);

# ENTENDIENDO A LOS CLIENTES

# Para analizar a nivel de cliente lo mejor es crear un dataframe de solo compradores con granularidad cliente y las variables que nos interesan.
# Hay que tener cuidado con la función de agregación que usamos en cada una.

clientes = df.loc[df.evento == 'purchase'].groupby(['usuario']).agg({'producto':'count',
                                                          'sesion':'nunique', 
                                                          'precio': 'mean',
                                                          'date': 'max'})

clientes.columns = ['productos_tot_num','compras_tot_num','precio_medio_prod','ult_compra']
print(clientes)

# Vamos a calcular variables adicionales.

clientes['gasto_tot'] = clientes.productos_tot_num * clientes.precio_medio_prod
clientes['productos_por_compra'] = clientes.productos_tot_num / clientes.compras_tot_num
print(clientes)

# ¿Cómo se distribuyen los clientes en cuánto a gasto?

sns.histplot(data = clientes, x = 'gasto_tot', bins = 50)
plt.xlim([0,300]);

# La gran mayoría de los clientes han gastado menos de 50€ en el período.

# ¿Cómo se distribuyen los clientes en cuanto al número de compras?

sns.countplot(data = clientes, x = 'compras_tot_num');

# INSIGHT #3: La gran mayoría de los clientes sólo hace una compra.

# Existe gran recorrido para mejorar este ratio mediante:
# Por ejemplo, email marketing con newletters y ofertas personalizadas

# ¿Cuántos productos compra un cliente de media en cada compra?

print(clientes.productos_por_compra.describe())

# INSIGHT #4 La compra mediana incluye 5 productos.
# Pero un 25% de los clientes compran más de 10 productos en la misma compra.

# Existe gran recorrido para mejorar este ratio mediante:
# Por ejemplo, sistemas de recomendación en el momento de la compra

# ¿Qué clientes nos han generado más ingresos?

clientes.nlargest(n = 10, columns = 'gasto_tot')

# Para calcular calculamos el gasto total medio por cliente.

print(clientes.gasto_tot.describe())

# INSIGHT #5 Existen clientes con gasto medio decenas de veces superior a la media.
# Hay que fidelizar estos clientes mediante programas de fidelización.
