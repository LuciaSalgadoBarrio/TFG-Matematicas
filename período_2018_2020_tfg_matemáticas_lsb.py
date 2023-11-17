# -*- coding: utf-8 -*-
"""Período 2018-2020 TFG Matemáticas LSB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_62Wu-9xDjM_XkSgFieehOIGCfABYWJG
"""

# Importamos las bibliotecas necesarias
import yfinance as yf
import datetime
import numpy as np
import pandas as pd

# Símbolos o tickers de las empresas del IBEX 35 escogidas en el estudio en forma de lista
symbols = [
    "ACS.MC", "ACX.MC", "AENA.MC", "ALM.MC", "AMS.MC", "ANA.MC", "BBVA.MC", "BKT.MC", "CABK.MC",
    "CLNX.MC", "COL.MC", "ELE.MC","ENG.MC", "FDR.MC", "FER.MC", "GRF.MC", "IAG.MC", "IBE.MC", "IDR.MC",
    "ITX.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "MTS.MC", "NTGY.MC", "REP.MC", "ROVI.MC", "SAB.MC", "SAN.MC", "SCYR.MC",
    "SLR.MC", "TEF.MC", "UNI.MC",
]

# Definimos las variables fecha inicial y fecha final
start_date = datetime.datetime(2018, 1, 1)
end_date = datetime.datetime(2020, 1, 1)

# Función para obtener el valor o precio de cierre para cada símbolo (empresa del IBEX 35)
close_data = {}
for symbol in symbols:
    data = yf.download(symbol, start=start_date, end=end_date)
    close_data[symbol] = data["Close"]

# Obtenemos todas las fechas únicas
dates = pd.date_range(start=start_date, end=end_date, freq="B")

# Creamos la matriz de valores de cierre
num_dates = len(dates)
num_symbols = len(symbols)
close_matrix = np.zeros((num_dates, num_symbols+1))
close_matrix[:, 0] = dates

for i, symbol in enumerate(symbols):
    close_prices = close_data[symbol].reindex(dates)
    close_matrix[:, i+1] = close_prices.values

# Imprimir y mostrar la matriz con los precios de cierre diarios para cada empresa
column_names = ['Fecha'] + symbols
df = pd.DataFrame(close_matrix, columns=column_names)
df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date  # Convertir las fechas a formato "yyyy-mm-dd"
print(df)

import numpy as np

# Obtener todas las columnas excepto la primera, es decir, eliminamos la columna con las fechas
close_matrix_columns = close_matrix[:, 1:]

# Mostrar las columnas obtenidas
column_names = symbols
df1 = pd.DataFrame(close_matrix_columns, columns=column_names)
print(df1)

import numpy as np

# Seleccionar todas las filas excepto la última, ya que no obtiene el valor de la última fila (referente a la fecha final)
selected_rows = close_matrix_columns[:-1, :]

# Mostrar las filas seleccionadas
df2 = pd.DataFrame(selected_rows, columns=symbols)
print(df2)

correlation_matrix = df2.corr()
print(correlation_matrix)

# Obtener los nombres de las columnas
nombres_columnas = correlation_matrix.columns
print("Nombres de las columnas:", nombres_columnas)

# Obtener los nombres de las filas (índice)
nombres_filas = correlation_matrix.index
print("Nombres de las filas:", nombres_filas)

import numpy as np
import matplotlib.pyplot as plt

# Elección del umbral óptimo dada una matriz de correlación
def calcular_matriz_adyacencia(correlation_matrix, threshold):
    matriz_adyacencia = np.where(np.abs(correlation_matrix) > threshold, 1, 0)
    return matriz_adyacencia
# Dividimos por 2 para evitar contar las aristas duplicadas
def contar_aristas(matriz_adyacencia):
    return int(np.sum(matriz_adyacencia) / 2)

#El umbral irá desde 0 hasta 1, de milésima en milésima
thresholds = np.arange(0, 1.1, 0.001)
num_aristas = []

for threshold in thresholds:
    matriz_adyacencia = calcular_matriz_adyacencia(correlation_matrix, threshold)
    num_aristas.append(contar_aristas(matriz_adyacencia))
#Creamos el gráfico que nos relacione el número de aristas del grafo en función del umbral
plt.plot(thresholds, num_aristas)
plt.xlabel('Umbral')
plt.ylabel('Número de aristas')
plt.title('Número de aristas en función del umbral 2018-2020')
plt.axis([0.5,1,0,300])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()

plt.show()

# Crear matriz de adyacencia, donde nos devuelva 1 si el valor del índice de correlación de Pearson es mayor que 0,75 y 0 en caso contrario.
matriz_adyacencia = np.where(np.abs(correlation_matrix) > 0.90, 1, 0)

# Convertimos la matriz de adyacencia a DataFrame
df_adyacencia = pd.DataFrame(matriz_adyacencia, columns=correlation_matrix.columns, index=correlation_matrix.index)

# Imprimimos la matriz de adyacencia
print(df_adyacencia)

import networkx as nx
import pandas as pd
# Crear el grafo a partir del DataFrame
G = nx.from_pandas_adjacency(df_adyacencia)
# Quitar las aristas que van de un nodo a sí mismo
self_edges = [(u, v) for (u, v) in G.edges() if u == v]
G.remove_edges_from(self_edges)

# Imprimir información del grafo
print("Número de nodos:", G.number_of_nodes())
print("Número de aristas:", G.number_of_edges())
print("Lista de aristas:", G.edges())

import matplotlib.pyplot as plt

# Representar el grafo
pos = nx.spring_layout(G)  # Calcular la posición de los nodos
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold', edge_color='black')

# Mostrar el grafo
plt.title("Grafo")
plt.axis('off')
plt.show()

#Tipo de diseño del grafo
pos_p1 = nx.circular_layout(G)

#Grosor de las aristas
edge = [0.2*G.get_edge_data(u, v)['weight'] for u, v in G.edges()]
#Espacio de representación
x, y = plt.subplots(figsize=(12, 12))
#Título del grafo
y.set_title("Período 2018-2020", dict(fontweight="bold",fontsize=22,color="black"),loc="center")

#Representación de los objetos del grafo
    #Aristas
nx.draw_networkx_edges(G, pos_p1, width=edge, edge_color="navy", style='-')
    #Nodos
nx.draw_networkx_nodes(G, pos_p1, node_size=700, node_shape='o', node_color="red", linewidths=1,edgecolors="black")
    #Etiquetas sobre nodos
nx.draw_networkx_labels(G, pos_p1, font_size=11, bbox=dict(ec="black",boxstyle="round",facecolor="white",pad=0.3,alpha=0.6), font_weight='normal', font_family='Arial', horizontalalignment='center', verticalalignment='center',clip_on=False)

#Modificaciones sobre el espacio de representación

plt.axis("off")
y.margins(0.05,0.05)
plt.savefig("G.png")
plt.show()

num_aristas = G.number_of_edges()

print("Número de nodos:", G.number_of_nodes())
print("Número de aristas:", G.number_of_edges())

#Identificamos los nodos aislados y que no formaran parte del estudio
isolated_nodes = [node for node in G.nodes if len(list(G.neighbors(node))) == 0]
#Eliminamos los nodos aislados anteriormente identificados
G.remove_nodes_from(isolated_nodes)

#Representamos el grafo sin nodos aislados
#Tipo de diseño del grafo
pos_p1 = nx.circular_layout(G)

#Grosor de las aristas
edge = [0.2*G.get_edge_data(u, v)['weight'] for u, v in G.edges()]
#Espacio de representación
x, y = plt.subplots(figsize=(12, 12))
#Título del grafo
y.set_title("Período 2018-2020", dict(fontweight="bold",fontsize=22,color="black"),loc="center")

#Representación de los objetos del grafo
    #Aristas
nx.draw_networkx_edges(G, pos_p1, width=edge, edge_color="navy", style='-')
    #Nodos
nx.draw_networkx_nodes(G, pos_p1, node_size=700, node_shape='o', node_color="red", linewidths=1,edgecolors="black")
    #Etiquetas sobre nodos
nx.draw_networkx_labels(G, pos_p1, font_size=11, bbox=dict(ec="black",boxstyle="round",facecolor="white",pad=0.3,alpha=0.6), font_weight='normal', font_family='Arial', horizontalalignment='center', verticalalignment='center',clip_on=False)

#Modificaciones sobre el espacio de representación

plt.axis("off")
y.margins(0.05,0.05)
plt.savefig("G.png")
plt.show()
num_aristas = G.number_of_edges()
print("Número de nodos:", G.number_of_nodes())
print("Número de aristas:", G.number_of_edges())

# Conseguimos las 8 primeras iteraciones del algoritmo
import networkx.algorithms.community as nx_comm
from networkx.algorithms import community
import itertools

lista_communities = []
num_it = 7
comp = community.girvan_newman(G)
for communities in itertools.islice(comp, num_it):
    print(tuple(sorted(c) for c in communities))
    lista_communities.append(tuple(sorted(c) for c in communities))


# Creamos el dendrograma correspondiente.

import networkx as nx
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

Nodes=np.array(list(G.nodes()))
G0=nx.Graph()
for link in G.edges:
    i0=np.where(Nodes==link[0])[0][0]
    i1=np.where(Nodes==link[1])[0][0]
    G0.add_edge(i0,i1)

N = G0.number_of_nodes();
m=len(G0.edges()); Ncomp=2; gn_alg=[[set(G0.nodes)]]; edges=[0]
for i in range(m):
    re=np.array(list(G0.edges))[np.argmax(np.array(list(nx.edge_betweenness_centrality(G0).values())))]
    G0.remove_edge(re[0],re[1])
    if nx.number_connected_components(G0)==Ncomp:
        Ncomp+=1; step=[]
        for comp in nx.connected_components(G0):
            step.append(comp)
        gn_alg=gn_alg+[step]
        edges=edges+[i+1]


CLUSTERS=[]; s=len(gn_alg);
for k in range(s-1):
    step=gn_alg[-2-k]
    cluster=list(step[np.where(np.array([len(l) for l in step])==2)[0][0]])
    CLUSTERS.append([float(cluster[0]),float(cluster[1]),float(m+1-edges[-1-k]),0]);
    for j in range(k+1,s-1):
        for l in gn_alg[-2-j]:
            if cluster[0] in l:
                l.remove(cluster[0]); l.remove(cluster[1]); l.add(N+k)
Nodes_labels=[]
for node in Nodes:
    Nodes_labels.append(node[:-3])

plt.figure(1,figsize=[10,10])

hierarchy.dendrogram(CLUSTERS, labels=Nodes_labels,color_threshold= 27)
Y=np.array(range(m+1))
plt.yticks(Y,m-Y)
plt.show()

plt.figure(1,figsize=[10,10],clear=True)
nx.draw_networkx(G, node_size=600, font_size=10)