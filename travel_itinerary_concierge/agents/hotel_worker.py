from data.catalog import hotel_options
class HotelWorker:
    name = "Hotel Worker"
    def find_hotels(self, request):
        return hotel_options(request.destination, request.days, request.hotel_category)
