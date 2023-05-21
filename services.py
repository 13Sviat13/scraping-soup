from pathlib import Path

import pandas as pd
import requests
from configurations import basedir
from bs4 import BeautifulSoup


class ScrapeMoviesService:

    url = "https://www.imdb.com/chart/top"

    def get_top_movies(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        poster_tags = soup.find_all('td', class_="posterColumn")
        title_tags = soup.find_all('td', class_="titleColumn")
        rating_tags = soup.find_all('td', class_="ratingColumn imdbRating")

        assert len(poster_tags) == len(title_tags) == len(rating_tags) == 250, "Error occurred while scrapping" # noqa

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

    def parse_poster_image(self, tag):
        return tag.find('img')['src']

    def parse_title(self, tag):
        return tag.find('a').text

    def parse_year(self, tag):
        return int(tag.find('span').text.lstrip('(').rstrip(')').strip())

    def parse_rating(self, tag):
        return float(tag.find('strong').text.strip())


if __name__ == '__main__':
    service = ScrapeMoviesService()
    top_movies = service.get_top_movies()

    df = pd.DataFrame.from_dict(top_movies)
    output_file_path = Path(basedir) / 'movies.csv'
    df.to_csv(output_file_path)


class ScrapeTVShowsService:

    url = "https://www.imdb.com/chart/tvmeter"

    def get_top_TVShows(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        image_tags = soup.find_all('td', class_="posterColumn")
        name_tags = soup.find_all('td', class_="titleColumn")
        rating_tags = soup.find_all('td', class_="ratingColumn imdbRating")

        assert len(image_tags) == len(name_tags) == len(rating_tags) == 100, "Error occurred while scrapping" # noqa

        results_TV = []
        for i in range(len(image_tags)):
            image = self.parse_image(tag=image_tags[i])
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

    def parse_image(self, tag):
        image_tag = tag.find('img')
        if image_tag is not None:
            return image_tag['src']
        return ""

    def parse_title(self, tag):
        title_tag = tag.find('a')
        if title_tag is not None:
            return title_tag.text
        return ""

    def parse_year(self, tag):
        year_tag = tag.find('span')
        if year_tag is not None:
            year_text = year_tag.text.lstrip('(').rstrip(')').strip()
            if year_text.isdigit():
                return int(year_text)
        return 0

    def parse_rating(self, tag):
        strong_tag = tag.find('strong')
        if strong_tag is not None:
            rating_text = strong_tag.text.strip()
            if rating_text.replace('.', '').isdigit():
                return float(rating_text)
        return 0.0


if __name__ == '__main__':
    service = ScrapeTVShowsService()
    top_TVShows = service.get_top_TVShows()

    df = pd.DataFrame.from_dict(top_TVShows)
    output_file_path = Path(basedir) / 'TVShows.csv'
    df.to_csv(output_file_path)
