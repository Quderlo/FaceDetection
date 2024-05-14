from django.urls import path
from .views import PersonsTableView, SightingListView, MainView, WebcamPageView

urlpatterns = [
    path('', MainView.as_view(), name="index"),
    path('persons/', PersonsTableView.as_view(), name='persons_table'),
    path('sightings/<int:person_id>/', SightingListView.as_view(), name='sighting_list'),
    path('webcam/', WebcamPageView.as_view(), name='webcam_page'),
]