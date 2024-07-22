import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from eld_app.helper.check_hos_violation import create_eld_data
from eld_app.models import ELD


def get_eld_data(request):
    return JsonResponse(
        list(ELD.objects.all().values('driver__driver_id', 'vehicle__vehicle_id', 'timestamp', 'status', 'location',
                                      'notes', 'start_time', 'end_time', 'duration')), safe=False)


@csrf_exempt
def create_new_schedule(request):
    if not request.method == 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=405)
    try:
        data = json.loads(request.body)
        response_data = create_eld_data(data)
        return JsonResponse(response_data, safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
