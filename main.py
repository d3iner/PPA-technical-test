import heapq
import itertools
from datetime import time, datetime, timedelta

from src.constants.constants import FLIGHT_ROUTES, FLIGHT_ITINERARY


def dijkstra( start, end):
    # Se inicializa la fila con el registro de los caminos
    queue = [(0, start)]  # (distance to start, node)
    # Se inicializa la lista de prioridad, todos los valores empiezan con
    distances = {node: float('infinity') for node in FLIGHT_ROUTES}
    # El nodo inicial se le asigna el valor de 0, para iniciar la busqueda del camino mas corto
    distances[start] = 0
    # Se inicializa un dict en el cual registraremos los nodos ya visitados
    previous_nodes = {node: None for node in FLIGHT_ROUTES}

    # Se crea un bucle infinito el cual parara una vez obtengamos el resultado que buscamos
    while queue:
        # Se obtiene el nodo con la distancia mas corta
        current_distance, current_node = heapq.heappop(queue)

        # Salimos del bucle si alcanzamos el nodo buscado
        if current_node == end:
            break

        # Exploracion de nodos vecinos
        for neighbor, weight in FLIGHT_ROUTES[current_node].items():
            distance = current_distance + weight

            # Solo se concidera esta ruta si es mejor o mas corta que la anterior
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Se recontruye el camino hecho
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path = path[::-1]  # Se invierte

    return distances[end], path

# Añade minutos a un objeto tipo time
def add_minutes_to_time(t = time(), minutes = 0.0):
    return (datetime.combine(datetime.today(), t) + timedelta(minutes=minutes)).time()

# Castea un time a un string con formato
def string_time(t = time()):
    return t.strftime('%H:%M')

# Imprime el mensaje por defecto cuando no hay resultados
def not_found_message():
    print("Tristemente para esta fecha no tenemos vuelos disponibles para este destino :(")

if __name__ == "__main__":
    print("BIENVENIDO A Punto de pago Airlines: \n\n")
    while True:
        try:
            print("Selecciones entre las siguientes opciones: \n")
            print("Presiona enter para encontrar ruta mas cercana entre 2 aereopuertos")
            print("Presiona Q + enter para salir \n")
            option = input()
            if option.upper() == 'Q':
                break
            print("\n")

            date_string = input("Ingresa la fecha del viaje (YYYY-MM-DD): ")
            #Se castea el string agregado (En el formato espesisicado) a una fecha
            date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
            #Se obtiene el dia de la semana
            day_of_week = date_obj.strftime("%A")

            # Se obtiene el intinerario disponible basado en el dia de semana
            day_flights = FLIGHT_ITINERARY.get(day_of_week)

            # Se obtienen los aereopuertos disponibles para verificar los valores ingresados
            airports = list(FLIGHT_ROUTES.keys())

            print(f"\nAereopuertos disponibles: {', '.join(airports)}")

            startAirport = input("\nIngrese el aereopuerdo desde el cual desea partir: ").upper()
            endAirport = input("\nIngrese el aereopuerdo de destino: ").upper()


            if not(startAirport in airports) or not(endAirport in airports):
                raise TypeError("Alguno o ambos aereopuertos que se buscan no existen")

            # Se hace uso del algoritmo de dijkstra para obtener cuanto dura la distancia mas corta y sus escalas
            duration, nodes = dijkstra(startAirport, endAirport)

            # Se divide el flujo entre la busqueda con al menos una escala, y las que son vuelos directos
            if len(nodes) == 2:
                flight_from = nodes[0]
                flight_to = nodes[-1]
                filtered_flights = [flight for flight in day_flights if flight['from'] == flight_from and flight['to'] == flight_to]

                print("\n")
                #En caso de no encontrar vuelos, se muestra el mensaje de no encontrado
                if len(filtered_flights) == 0:
                    not_found_message()
                else:
                    # Se iteran todos los vuelos encontrados para imrpimirlos
                    for flight in filtered_flights:
                        departure = time(flight['departure_hour'], flight['departure_minute'])
                        arrival = add_minutes_to_time(departure, duration)
                        print(f"{flight_from} -> {flight_to} - {string_time(departure)} | El tiempo de vuelo es de aproximadamente {duration} minutos | Tiempo de llegada aproximado a las {string_time(arrival)}")
            else:
                # Se obtiene lugar de inicio y de destino final basado en los nodos
                flight_from = nodes[0]
                flight_to = nodes[-1]

                # Se filtra la busqueda para que solo queden los vuelos con origen o destino que esten incluidos en el nodo de camino mas corto y que no rompen con la unidireccionalidad (Solo le toman los vuelos que sirven para hacer el camino de ida y no al reves)
                filtered_flights = [
                    flight for flight in day_flights
                    if flight['from'] in nodes and flight['to'] in nodes and nodes.index(
                        flight['from']) < nodes.index(flight['to'])
                ]
                # Se ordena por hora para crear las escalas
                filtered_flights.sort(key=lambda x:(x["departure_hour"], x["departure_minute"]))

                flights = []

                # Se agrupan los vuelos de la primera es cala y los de segunda escala
                for i in range(len(nodes) -1):
                    flights.append([flight for flight in filtered_flights if flight['from'] == nodes[i] and flight['to'] == nodes[i+1]])

                # En caso que no hayan vuelos, o que no existan suficientes vuelos de escala, se toma como no encontrado
                if len(filtered_flights) == 0 or not all(len(flight) > 0 for flight in flights):
                    not_found_message()
                print('')
                #Se iteran todas las posibles combinaciones posibles de la lista armada
                for route in list(itertools.product(*flights)):
                    valid = True

                    #V Verificamos que en la cobinacion hecha, los vuelos de escala sean lo suficientemente despues de los anteriores para poder tomarlo como ruta valida
                    for i in range(1, len(route)):
                        actual = route[i]
                        preview = route[i-1]
                        last_distance, path = dijkstra(preview['from'], actual['from'])
                        actual_hour = actual['departure_hour'] * 60 +  actual['departure_minute'] + last_distance
                        preview_hour = preview['departure_hour'] * 60 +  preview['departure_minute']
                        if actual_hour < preview_hour:
                            valid = False
                            break
                    # En caso de ser valido, se imprimen las posibles opciones
                    if valid:
                        string_path = [f"{r['from']}->{r['to']}" for r in route]
                        string_times = [f"{string_time(time(r['departure_hour'], r['departure_minute']))}" for r in route]
                        departure = time(route[-1]['departure_hour'], route[-1]['departure_minute'])
                        arrival = add_minutes_to_time(departure, duration)
                        print(f"{', '.join(string_path)} - {', '.join(string_times)} | El tiempo de vuelo total es de aproximadamente {duration} minutos sin tener en cuenta tiempo de espera entre escalas | Tiempo de llegada aproximado a su destino final a las {arrival.strftime('%H:%M')}")
        except ValueError:
            print('\nFecha ingresada con el formato equivocado')
        except TypeError:
            print('\nAlguno o ambos aereopuertos que se buscan no existen')
        except:
            print('\nError desconocido')
        print("\n \n")
        input("\nPresione enter para volver al inicio")
