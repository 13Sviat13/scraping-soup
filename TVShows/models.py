from django.db import models


class TVShows(models.Model):
    image = models.URLField()
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    rating = models.FloatField()

    def __repr__(self):
        return f"{self.name} ({self.year})"
