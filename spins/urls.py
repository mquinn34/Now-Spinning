from django.urls import path
from .views import SpinCreateView, discogs_search

urlpatterns = [
    path('new/', SpinCreateView.as_view(), name='create_spin'),
    path('search-discogs/', discogs_search, name='discogs_search'),
]
