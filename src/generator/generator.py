# Archivo creado con proposito de generar un itinerario de vuelo aleatoriamente

from random import randint

from src.constants.constants import FLIGHT_ROUTES

def generate_itinerary():
    flight_routes = FLIGHT_ROUTES
    keys = list(flight_routes.keys())
    values = list(flight_routes.values())

    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    itinerary = dict({})

    for day_of_the_week in days_of_the_week:
        itinerary[day_of_the_week] = []
        for i in range(50):
            hour = randint(0, len(flight_routes) - 1)
            minute = randint(0, 3) * 15
            from_airport = keys[randint(0, len(flight_routes) - 1)]
            destinations = list(flight_routes[from_airport].keys())

            to_airport = destinations[randint(0, len(destinations) - 1)]
            itinerary[day_of_the_week].append({
                "from": from_airport,
                "to": to_airport,
                "departure_hour": hour,
                "departure_minute": minute
            })
    return itinerary

if __name__ == "__main__":
    flight_itinerary = generate_itinerary()

    print(flight_itinerary)
