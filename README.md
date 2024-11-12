# PPA

Bievenido a Punto de Pago Airlines, este proyecto consiste un algoritmo para encontrar la ruta más corta entre dos aeropuertos, utilizando grafos cuyos nodos representan los aereopuertos disponibles y el uso del algoritmo de Dijkstra el cual nos permite encontrar la ruta mas cercana entre los aereopuertos aunque no esten conectados directamente.

## Descripción

El objetivo principal es ayudar a los usuarios a encontrar la ruta más corta entre dos aeropuertos. Usando el algoritmo de Dijkstra, el codigo evalúa todas las rutas posibles y elige la de menor peso (tiempo) entre un aeropuerto de origen y uno de destino.

A continuacion se presenta el grafo que representa los aereopuertos y sus rutas

![Graph](src/assets/graph.png)

Como podemos notar hay varios aereopuertos  los cuales no estan conectados directamente, y el algoritmo de Dijkstra busca encontrar una ruta indirecta entre esos aereopuertos que estan coneectados, y los que no, ademas de conseguir sus rutas mas cortas


## Funcionalidades

- Cálculo de la ruta más corta entre dos aeropuertos.
- Visualización de la ruta óptima, posibles intinerarios y tiempo de vuelo.


## Uso

1. Ejecuta el archivo principal:
    ```bash
    python main.py
    ```

2. Por medio de la terminal, esocoge las opciones permitidas. 
3. En caso de escoger la opcion de busqueda de vuelo, ingrese la fecha de viaje en el formato indicado, y acontinuacion escoge los aeropuertos de origen y destino los cuales desea.
4. El sistema calculará y mostrará la ruta más corta entre los aeropuertos, y las opciones que tiene como posible intinerario.



