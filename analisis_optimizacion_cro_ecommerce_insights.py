# -*- coding: utf-8 -*-

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

# ¿Cual es la supervivencia de los clientes?

# Dado que solo tenemos 5 meses de histórico vamos a crear análisis de cohortes a 3 meses vista, lo cual nos da para hacer 3 cohortes.
# Preparamos un dataframe solo con compradores y con las variables usuario y mes.


c = df.loc[df.evento == 'purchase', ['usuario','mes']]
c = pd.crosstab(c.usuario,c.mes).reset_index()

print(c)

# Renombramos y eliminamos el usuario que ya no lo necesitamos.

c.columns = ['usuario','c4','c5','c1','c2','c3']
c.drop(columns = 'usuario', inplace = True)

# La primera cohorte será la del mes 2, ya que queremos seleccionar "nuevos" clientes (al menos que no estuvieran el mes anterior)

c2 = c.loc[(c.c1 == 0) & (c.c2 > 0)]

# Pasamos a un dataframe binario ya que solo nos importa si ese cliente ha comprado o no en cada mes.

def binarizar(variable):
    variable = variable.transform(lambda x: 1 if (x > 0) else 0)
    return(variable)

c2_b = c2.apply(binarizar)

# Calcumamos el porcentaje de clientes de esta cohorte que han seguido comprando en los siguientes meses.

c2_f = c2_b.sum() / c2_b.shape[0]
c2_f = c2_f.sort_index()
print(c2_f)

# Replicamos todo el proceso para la cohorte 3

c3 = c.loc[(c.c2 == 0) & (c.c3 > 0)]
c3_b = c3.apply(binarizar)
c3_f = c3_b.sum() / c3_b.shape[0]
c3_f = c3_f.sort_index()
c3_f['c1'] = 0
print(c3_f)


# Replicamos todo el proceso para la cohorte 4

c4 = c.loc[(c.c3 == 0) & (c.c4 > 0)]
c4_b = c4.apply(binarizar)
c4_f = c4_b.sum() / c4_b.shape[0]
c4_f = c4_f.sort_index()
c4_f['c1'] = 0
c4_f['c2'] = 0
print(c4_f)

# Creamos el dataframe de cohortes.

cohortes = pd.DataFrame({'c2':c2_f,'c3':c3_f,'c4':c4_f})
cohortes = cohortes.drop(index = 'c1').T
print(cohortes)

plt.figure(figsize = (12,6))
sns.heatmap(cohortes,annot = True, fmt = '.0%', cmap='Greys');

# INSIGHT #6: El 90% de que los nuevos clientes no vuelve a comprar en los meses posteriores

# ¿Cual es el LTV de los clientes?

# Teniendo en cuenta el 90% de que los nuevos clientes no vuelve a comprar en los meses posteriores podemos calcular el LTV con el histórico que tenemos sin miedo a equivocarnos mucho.
# Para ello vamos a coger a los clientes de la cohorte 2 y calcular el total de sus compras.

maestro_ltv = df.loc[(df.evento == 'purchase') & (df.mes != 10) & (df.mes == 11),'usuario'].to_list()

clientes_ltv = clientes.loc[clientes.index.isin(maestro_ltv)]

print(clientes_ltv.gasto_tot.describe())

# Dada la variabilidad de la media sería más seguro coger la mediana.

# INSIGHT #7: El LTV medio es de 42€.

# Aplicando nuestro margen sobre esa cifra y el % que queremos dedicar a captación nos sale el importe máximo a invertir en CPA.
# Aplicar las acciones de CRO permitirá incrementar el LTV y por tanto también el CPA, siendo una ventaja estratégica muy importante.

# ¿Sobre qué clientes ejecutar las próximas campañas (RFM)?

"""
Vamos a aprender una técnica llamada RFM (Recency - Frequency - Monetary).

Esta técnica es muy potente para contextos de retail y por tanto también en ecommerce.

Permite dar respuesta a necesidades como:

Cuál es la proporción de clientes que realizan un solo pedido y clientes frecuentes
Cuales son los clientes VIP (que potencialmente necesitan programas de fidelización y atención personalizada)
Cuál es la cantidad de clientes nuevos (a incentivar para que vuelvan a realizar un pedido)
Cuántos y cuáles son los clientes que no realizan compras hace tiempo
Cuántos y cuáles son los clientes en los cuales no vale la pena invertir más tiempo y recursos
Etc
Pese a su potencia es muy sencilla de construir, por tanto es casi obligatoria en este tipo de análisis.

Lo primero es identificar las variables con las que crear cada una de las dimensiones:

Recency: ult_compra
Frequency: compras_tot_num
Monetary: gasto_tot
Y discretizar cada una de ellas.

Vamos a dejar la recencia para el final porque requerirá una transformación previa.
"""

# Comenzamos por Frequency

clientes['F'] = clientes.compras_tot_num.transform(lambda x: pd.cut(x,5, labels = False)) + 1
clientes.groupby('F').compras_tot_num.mean()

# Ahora Monetary

clientes['M'] = clientes.gasto_tot.transform(lambda x: pd.cut(x,5, labels = False)) + 1
clientes.groupby('M').gasto_tot.mean()

# Para la recencia tenemos que transformar la fecha a un número, por ejemplo la distancia en días de cada fecha a la fecha más reciente disponible.

mas_reciente = clientes.ult_compra.max()
clientes['ult_compra_dias'] = clientes.ult_compra.transform(lambda x: mas_reciente - x)

# Nos ha creado un timedelta, tenemos que pasarlo a número de días.

clientes['ult_compra_dias'] = clientes.ult_compra_dias.dt.days

# Ya podemos crear la R, pero hay que tener en cuenta que en este caso lo mejor son los valores más bajos.

clientes['R'] = clientes.ult_compra_dias.transform(lambda x: pd.cut(x,5, labels = False)) + 1
clientes.groupby('R').ult_compra_dias.mean()

# Para estandarizar su intrepretación con el resto de las dimensiones vamos a darle la vuelta.

clientes['R'] = 6 - clientes.R
clientes.groupby('R').ult_compra_dias.mean()

# Integramos en un dataframe rfm.

clientes['valor'] = clientes.R + clientes.F + clientes.M
clientes['RFM'] = clientes.apply(lambda x: str(x.R) + str(x.F) + str(x.M), axis = 1)
clientes

# Sobre este dataframe ya podemos hacer infinidad de análisis.
# Por ejemplo combinándolo con la técnica del minicubo podemos obtener todo tipo de insights.

# PASO 1: Seleccionar qué variables serán la métricas y cuales las dimensiones
metricas = ['productos_tot_num','compras_tot_num','gasto_tot']
dimensiones = ['R','F','M','RFM','valor']

minicubo = clientes[dimensiones + metricas]
print(minicubo)

# PASO 2: pasar a transaccional las dimensiones
minicubo = minicubo.melt(id_vars = metricas)
print(minicubo)

# PASO 3: Agregar las métricas por "variable" y "valor" con las funciones deseadas
minicubo = minicubo.groupby(['variable','value'], as_index = False)[metricas].mean()
print(minicubo)

# Para analizar cada dimensión la seleccionamos.

minicubo[minicubo.variable == 'F']
minicubo[minicubo.variable == 'F'].set_index('value').plot.bar(subplots = True, sharex = False, figsize = (12,12))
plt.tight_layout();

minicubo[minicubo.variable == 'R']
minicubo[minicubo.variable == 'R'].set_index('value').plot.bar(subplots = True, sharex = False, figsize = (12,12))
plt.tight_layout();

minicubo[minicubo.variable == 'M']
minicubo[minicubo.variable == 'M'].set_index('value').plot.bar(subplots = True, sharex = False, figsize = (12,12))
plt.tight_layout();

minicubo[minicubo.variable == 'RFM']
minicubo[minicubo.variable == 'RFM'].set_index('value').plot.bar(subplots = True, sharex = False, figsize = (12,12))
plt.tight_layout();

minicubo[minicubo.variable == 'valor']
minicubo[minicubo.variable == 'valor'].set_index('value').plot.bar(subplots = True, sharex = False, figsize = (12,12))
plt.tight_layout();

# Se podría mejorar el análisis porque en F y M los atípicos hacen que se concentren la mayoría de los datos en la categoría 1.
# Lo que habría que hacer es eliminar esos atípicos y volver a realizar el ejercicio.

# Pero con este análisis somos capaces de identificar los clientes que con mayor probabilidad responderán mejor a nuevas campañas, además de obtener un montón de insights valiosos para el negocio.

# ENTENDIENDO LOS PRODUCTOS

# Vamos a crear un dataframe a nivel de producto para poder analizar esta dimensión.
# Primero calculamos los conteos de cada evento en cada producto.

prod = df.groupby(['producto','evento']).size()
print(prod)

prod  = prod.unstack(level = 1).fillna(0)
print(prod)

# Vamos a incorporar el precio, para ello primero creamos un maestro de precios por producto.

maestro_precios = df.groupby('producto', as_index = False).precio.mean()
print(maestro_precios)

prod = pd.merge(left = prod, right = maestro_precios, how = 'left', on = 'producto')
print(prod)

# Reordenamos los nombres.

prod = prod[['producto','view','cart','remove_from_cart','purchase','precio']]

# ¿Cuales son los productos más vendidos?

prod.sort_values('purchase',ascending = False)[0:20]

# Posiblemente lograríamos incrementar las ventas y el ticket medio simplemente destacando estos productos en la tienda.

# ¿Hay productos que no se venden y podríamos eliminar del catálogo?

prod[prod.purchase == 0]

# INSIGHT #8: Casi la mitad de los productos no han tenido ninguna venta en los 5 meses del histórico.
# Se podría comenzar todo un nuevo análisis sobre estos productos:

# - ¿No se ven?
# - ¿Se ven pero no se compran?
# - ¿Es porque se sustituyen por otros productos propios?
# - ¿Es porque están mucho más baratos en la competencia?

# Se podrían eliminar del catálogo, o como mínimo de la tienda, newsletter, etc, para que no ocupen espacio de los productos que sí se venden.

# ¿Cual es la relación entre el precio y el volumen de ventas?
# Ya que este análisis incluye las ventas vamos a eliminar los productos que no han tenido ninguna.

sns.scatterplot(data = prod[prod.purchase > 0], x = 'precio', y = 'purchase', hue = 'precio');

# Sí que existe una clara relación decreciente.
# Vamos a hacer zoom por ejemplo por debajo de 50€ para entenderlo mejor.

sns.scatterplot(data = prod[(prod.purchase > 0) & (prod.precio < 50)], x = 'precio', y = 'purchase', hue = 'precio');

# Hay productos de los que los clientes se arrepienten y eliminan más del carrito?

prod.insert(loc = 4,
            column = 'remove_from_cart_porc',
            value = prod.remove_from_cart / prod.cart *100 )
print(prod)

prod.loc[prod.cart > 30].sort_values('remove_from_cart_porc', ascending = False)[0:30]

# Habría que ver por qué estos productos se eliminan más veces de las que se añaden:

# - Si el motivo tiene sentido: revisar qué pasa con estos productos (otros productos alternativos, etc.)
# - Si no lo tiene eliminar estos registros y analizar únicamente los que tienen remove_from_cart_porc menor o igual a 100

# ¿Cuales son los productos más vistos?

prod.view.sort_values(ascending = False)[0:20].plot.bar();

# Posiblemente lograríamos incrementar las ventas y el ticket medio simplemente destacando estos productos en la tienda.
# Siempre que además de ser vistos también se vendan.

# ¿Hay productos deseados pero no comprados?
# Por ejemplo productos que miran muchos clientes pero que luego no los compran.
# Si los encontráramos habría que revisar qué pasa con ellos.

sns.scatterplot(data = prod, x = 'view', y = 'purchase');

# Vamos a quitar el atípico y hacer zoom en la ventana de muchas vistas pocas compras.

sns.scatterplot(data = prod.loc[prod.view < 4000], x = 'view', y = 'purchase', hue = 'precio')
plt.xlim(1000,3000)
plt.ylim(0,150)

# Hay una oportunidad con estos productos, porque por algún motivo generan el interés de los clientes, pero finalmente no los compran.
# Habría que hacer un análisis sobre ellos.

# CONSTRUYENDO UN SISTEMA DE RECOMENDACIÓN

"""
Uno de los activos que más pueden incrementar las ventas de un ecommerce es un sistema de recomendación.

Ya podríamos aplicar uno básico con los análisis de más visto y más vendido realizados anteriormente.

Pero la verdadera potencia viene cuando creamos un recomendador que personaliza para cada compra.

Tipos de sistemas de recomendación:

Filtrado colaborativo:

- Basados en items
- Basados en usuario
- De contenido

En nuestro caso vamos a desarrollar uno con filtrado colaborativo basado en items.

Los pasos a seguir son:

- Crear el dataframe con el kpi de interés
- Reducir la dimensión (opcional)
- Seleccionar una métrica de distancia
- Calcular la matriz item-item
- Crear la lógica de priorización
"""

# Crear el dataframe con el kpi de interés

# En este caso usaremos lo que se llama un kpi implícito, que será el número de veces que los productos han sido comprados por el mismo usuario.
# Kpis explícitos sería por ejemplo estrellas o puntuaciones del 1 al 10.
# Dado que este es una algoritmo que tarda en calcularse vamos a reducir el problema y calcularlo solo para los 100 productos más vendidos.
# Además, por motivos didácticos vamos a hacer el paso a paso manualmente. En un uso real se recomienda usar un paquete ya preconstruído que posiblemente estará más optimizado en cuanto a rendimiento.

# Primero calculamos un maestro con los 100 productos más vendidos.

mas_vendidos = prod.sort_values('purchase', ascending = False).producto[0:100]

# Creamos un dataframe temporal filtrando por estos productos.

temp = df.loc[df.producto.isin(mas_vendidos)]

# Creamos la matriz  usuario-item.

usuario_item = temp.loc[temp.evento == 'purchase'].groupby(['usuario','producto']).size().unstack(level = 1).fillna(0)

# Reducir la dimensión (opcional)

# Vemos que nos ha salido una matriz sparse.
# Posiblemente sería conveniente reducir la dimensión con técnicas como SVD, pero eso requería un minicurso en sí mismo.
# Aquí vamos a continuar sin hacer la reducción.

# Seleccionar una métrica de distancia

# Métricas más comunes:

# - Distancia euclídea
# - Correlación
# - Coseno

# En este caso vamos a coger por ejemplo la distancia euclídea.
# La operativizamos mediante la función spatial.distance.euclidean de Scipy.

from scipy import spatial

# Calcular la matriz item-item

# Creamos el recomendador que toma como input una matriz usuario-item y devuelve una matriz item-item con la distancia euclídea como dato.

def recomendador(dataframe):

    def distancia(producto):
        return(dataframe.apply(lambda x: spatial.distance.euclidean(x,producto)))

    return(dataframe.apply(lambda x: distancia(x)))

item_item = recomendador(usuario_item)

# Crear la lógica de priorización

"""
Ya tenemos listo el recomendador.

Lo que tendríamos que hacer es una llamada a esta tabla cada vez que un usuario mire un producto o lo meta en el carrito.

Pero para que sea más efectivo podríamos usar toda la info acumulada de la sesión o incluso de todo el usuario si está logado.

Eso significa que necesitamos un sistema para recomendar productos tanto si el input es de un solo producto como de varios.

Y que a la vez devuelva varias recomendaciones, para cubrir todos los "huecos" de recomendación que nuestra web pudiera tener.

Aplicaremos un algoritmo muy sencillo que hará:

- Crear un array con los productos de entrada para extraer sus vectores de la matriz item-item
- Calcular la suma de distancias de todos los productos
- Quitarse a ellos mismos para no autorecomendarse.
- Devolver los 10 con menor distancia
"""

# En el caso de varios productos vendrá del servidor web como una cadena separada con punto y coma
def priorizador(productos,devuelve = 10):
    
    # Crear array con productos de entrada
    array = np.int64(productos.split(';'))
    
    # Extraer sus vectores de la matriz total
    matriz = item_item[array]
    
    # Calcular la suma de distancias
    suma_distancias = matriz.agg(sum,axis = 1)
    
    # Eliminar los productos input
    suma_distancias = suma_distancias.loc[~suma_distancias.index.isin(list(array))]
    
    # Devolver los 10 con menor distancia
    return(suma_distancias.sort_values()[0:devuelve])

# Comprobamos cómo funciona si le pasamos un producto

priorizador('4497')

# Comprobamos cómo funciona si le pasamos varios productos

priorizador('4497;4600;4768')

# CONCLUSIONES

# La tendencia actual es plana en todas las métricas, lo que confirma la necesidad de las acciones de CRO.
# Tras el análisis realizado sobre los datos transaccionales se ha desarrollado un plan CRO de 12 iniciativas concretas organizadas en 5 grandes palancas de negocio que con alta probabilidad van a incrementar los baselines consiguiendo un incremento global de los ingresos del ecommerce.

# BASELINE

# En cada sesión, de media:

# - KPIs por sesión: Se ven 2.2 productos
# - KPIs por sesión: Se añaden 1.3 productos al carrito
# - KPIs por sesión: Se eliminan 0.9 productos del carrito
# - KPIs por sesión: Se compran 0.3 productos
# - Venta cruzada: mediana de 5 productos por compra
# - Recurrencia: el 10% de los clientes vuelve a comprar tras el primer mes
# - Conversión: 60% de añadir al carrito sobre visualizaciones
# - Conversión: 22% de compra sobre añadidos a carrito
# - Conversión: 13% de compra sobre visualizaciones
# - Facturación media mensual: 125.000€

# ACCIONES DE INCREMENTO DE VISUALIZACIONES

# - Revisar las campañas de paid (generación y retargeting) para concentrar la inversión en franjas entre las 9 y las 13 y entre las 18 y las 20
# - Concentrar la inversión del período navideño y post-navideño en la semana del black friday
# - Incrementar la inversión hasta llegar al CPA máximo en base al LTV que hemos identificado

# ACCIONES DE INCREMENTO DE CONVERSIÓN

# - Preconfigurar la home con los productos identificados en los análisis most viewed y most sold.
# - Trabajar sobre los productos con alta tasa de abandono de carrito
# - Trabajar sobre los productos muy vistos pero poco comprados

# ACCIONES DE INCREMENTO DE VENTA CRUZADA

# - La compra mediana incluye 5 productos
# - Incrementar este ratio mediante la recomendación en tiempo real con el nuevo recomendador

# ACCIONES DE INCREMENTO DE FRECUENCIA DE COMPRA

# - El 90% de los clientes sólo hace una compra
# - Crear una newsletter periódica con el nuevo recomendador para incrementar la frecuencia de visita
# - Campañas promocionales sobre los segmentos top de la segmentación RFM

# ACCIONES DE FIDELIZACIÓN DE CLIENTES

# 12. Crear un programa de fidelización segmentado por la nueva segmentación RFM

