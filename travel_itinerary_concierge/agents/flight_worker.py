from data.catalog import flight_options
class FlightWorker:
    name = "Flight Worker"
    def find_flights(self, request):
        return flight_options(request.origin, request.destination)
