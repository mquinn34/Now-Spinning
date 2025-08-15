from django.urls import path
from .views import (
    SpinCreateView,
    discogs_search_artists,
    discogs_artist_releases,
)

urlpatterns = [
    path('new/', SpinCreateView.as_view(), name='create_spin'),
    path('api/discogs/artists', discogs_search_artists, name='discogs_search_artists'),
    path('api/discogs/artist/<int:artist_id>/releases', discogs_artist_releases, name='discogs_artist_releases'),
]
