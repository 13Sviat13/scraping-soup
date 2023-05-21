from django.shortcuts import render
from .models import TVShows


def top_TVShows(request):
    tvshows = TVShows.objects.all()

    context = {
        'TVShows': tvshows
    }
    return render(request, template_name='core/tvshows.html', context=context)
