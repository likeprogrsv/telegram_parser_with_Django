from django.db import models


class Picture(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url


class News(models.Model):
    resource = models.CharField(max_length=50)
    post_time = models.DateTimeField()
    tag = models.CharField(max_length=50)
    pictures = models.ManyToManyField(Picture)


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
