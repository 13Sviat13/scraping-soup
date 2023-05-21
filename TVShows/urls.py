from django.urls import path
from .views import top_TVShows


urlpatterns = [
    path('TVShows/', top_TVShows, name='TVShows')
]
