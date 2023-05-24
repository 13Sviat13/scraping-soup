from django.http import JsonResponse
from django.shortcuts import render

from services import IMDBService
from .models import TVShows


def top_TVShows(request):
    tvshows = TVShows.objects.all()

    context = {
        'TVShows': tvshows
    }
    return render(request, template_name='core/tvshows.html', context=context)


def scraping_data(request):
    category = request.GET['category']
    service = IMDBService.get_service(category=category)
    objects = service.get_TV_objects()
    data = service.persist_objectsTV(objects)

    return JsonResponse({'data': data})
