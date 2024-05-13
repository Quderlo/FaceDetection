from django.urls import path
from .views import persons_table_view, sighting_list_view, main, webcam_page

urlpatterns = [
    path('', main, name="index"),
    path('persons/', persons_table_view, name='persons_table'),
    path('sightings/<int:person_id>/', sighting_list_view, name='sighting_list'),
    path('webcam/', webcam_page, name='webcam_page'),
]