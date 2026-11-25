from data.catalog import activity_options
class ActivityWorker:
    name = "Activity Worker"
    def propose_activities(self, request):
        return activity_options(request.interests)
