from django.shortcuts import render
from services import ScrapeMoviesService, ScrapeTVShowsService
from movies.models import Movie
from TVShows.models import TVShows


def index(request):

    service_movie = ScrapeMoviesService()
    top_movies = service_movie.get_top_movies()
    service_tv = ScrapeTVShowsService()
    top_TVShows = service_tv.get_top_TVShows()

    # top_movies = []
    for top_movie in top_movies:
        movie = (
            Movie.objects
            .filter(
                title=top_movie.get('title'),
                year=top_movie.get('year')
            )
            .first()
        )
        if movie:
            movie.poster_image = top_movie.get('poster_image')
            movie.rating = top_movie.get('rating')
            movie.save()
        else:
            movie = Movie(
                poster_image=top_movie.get('poster_image'),
                title=top_movie.get('title'),
                year=top_movie.get('year'),
                rating=top_movie.get('rating')
            )
            movie.save()

    for top_TVShow in top_TVShows:
        TVShow = (
            TVShows.objects
            .filter(
                name=top_TVShow.get('name'),
                year=top_TVShow.get('year')
            )
            .first()
        )
        if TVShow:
            TVShow.image = top_TVShow.get('image')
            TVShow.rating = top_TVShow.get('rating')
            TVShow.save()
        else:
            top_TVShow = TVShows(
                image=top_TVShow.get('image'),
                name=top_TVShow.get('name'),
                year=top_TVShow.get('year'),
                rating=top_TVShow.get('rating')
            )
            top_TVShow.save()

    return render(request, 'core/index.html')
