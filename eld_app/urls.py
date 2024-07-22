from django.urls import path

from eld_app.views import get_eld_data, create_new_schedule

urlpatterns = [
    path('api/eld-data/', get_eld_data, name='eld_data'),
    path('api/show_violation/', create_new_schedule, name='show_violation'),
]
