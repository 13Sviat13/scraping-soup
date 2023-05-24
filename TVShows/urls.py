from django.urls import path
from .views import top_TVShows, scraping_data

urlpatterns = [
    path('', top_TVShows, name='TVShows'),
    path('scraping_data/', scraping_data, name='scraping_data')
]
