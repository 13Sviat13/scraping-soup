import pandas as pd
import requests
from bs4 import BeautifulSoup

from TVShows.models import TVShows
from confic.settings import BASE_DIR
from movies.models import Movie
from django.forms.models import model_to_dict


class IMDBService:

    MOVIES = 'movies'
    TVSHOWS = 'tvshows'

    def get_objects(self):
        raise NotImplementedError

    def persist_objects(self, objects):
        raise NotImplementedError

    @classmethod
    def get_service(cls, category):
        if category == cls.MOVIES:
            return ScrapeMoviesService()
        elif category == cls.TVSHOWS:
            return ScrapeTVShowsService()
        else:
            raise NotImplementedError

    def parse_poster_image(self, tag):
        """
        Parse image from posterColumn tag
        :param tag:
        :return:
        """
        return tag.find('img')['src']

    def parse_title(self, tag):
        return tag.find('a').text

    def parse_year(self, tag):
        return int(tag.find('span').text.lstrip('(').rstrip(')').strip())

    def parse_rating(self, tag):
        return float(tag.find('strong').text.strip())


class ScrapeMoviesService(IMDBService):
    url = "https://www.imdb.com/chart/top"

    def get_objects(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        poster_tags = soup.find_all('td', class_="posterColumn")
        title_tags = soup.find_all('td', class_="titleColumn")
        rating_tags = soup.find_all('td', class_="ratingColumn imdbRating")

        assert len(poster_tags) == len(title_tags) == len(rating_tags) == 250, "Error occurred while scrapping "

        results = []
        for i in range(len(poster_tags)):
            poster_image = self.parse_poster_image(tag=poster_tags[i])
            title = self.parse_title(tag=title_tags[i])
            year = self.parse_year(tag=title_tags[i])
            rating = self.parse_rating(tag=rating_tags[i])

            results.append(
                {
                    'poster_image': poster_image,
                    'title': title,
                    'year': year,
                    'rating': rating
                }
            )
        return results

    def persist_objects(self, objects):
        movies = []
        for top_movie in objects:
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
                    rating=top_movie.get('rating'),
                )
                movie.save()
            movies.append(model_to_dict(movie))
        return movies


if __name__ == '__main__':
    service = IMDBService.get_service(category=IMDBService.MOVIES)
    top_movies = service.get_objects()

    df = pd.DataFrame.from_dict(top_movies)

    output_file_path = BASE_DIR / 'movies.csv'
    df.to_csv(output_file_path)


class ScrapeTVShowsService(IMDBService):

    url = "https://www.imdb.com/chart/tvmeter"

    def get_TV_objects(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        image_tags = soup.find_all('td', class_="posterColumn")
        name_tags = soup.find_all('td', class_="titleColumn")
        rating_tags = soup.find_all('td', class_="ratingColumn imdbRating")

        assert len(image_tags) == len(name_tags) == len(rating_tags) == 100, "Error occurred while scrapping" # noqa

        results_TV = []
        for i in range(len(image_tags)):
            image = self.parse_poster_image(tag=image_tags[i])
            name = self.parse_title(tag=name_tags[i])
            year = self.parse_year(tag=name_tags[i])
            rating = self.parse_rating(tag=rating_tags[i])

            results_TV.append(
                {
                    'image': image,
                    'name': name,
                    'year': year,
                    'rating': rating
                }
            )
        return results_TV

    def persist_objectsTV(self, objects):
        tvshows = []
        for top_TVShows in objects:
            tvshow = (
                TVShows.objects
                .filter(
                    name=top_TVShows.get('name'),
                    year=top_TVShows.get('year')
                )
                .first()
            )
            if tvshow:
                tvshow.image = top_TVShows.get('image')
                tvshow.rating = top_TVShows.get('rating')
                tvshow.save()
            else:
                tvshow = TVShows(
                    image=top_TVShows.get('image'),
                    name=top_TVShows.get('name'),
                    year=top_TVShows.get('year'),
                    rating=top_TVShows.get('rating'),
                )
                tvshow.save()
            tvshows.append(model_to_dict(tvshow))
        return tvshows


if __name__ == '__main__':
    service = IMDBService.get_service(category=IMDBService.TVSHOWS)
    top_TVShows = service.get_TV_objects()

    df = pd.DataFrame.from_dict(top_TVShows)
    output_file_path = (BASE_DIR) / 'TVShows.csv'
    df.to_csv(output_file_path)
