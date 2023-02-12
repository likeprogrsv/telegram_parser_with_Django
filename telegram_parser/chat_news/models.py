from django.db import models
from django.conf import settings
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    content = models.TextField(blank=True)
    post_time = models.DateTimeField(default=timezone.now)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            related_name='posts')

    def __str__(self):
        return self.content


class Picture(models.Model):
    image = models.ImageField(upload_to=f'{settings.BASE_DIR}/'
                              f'{settings.MEDIA_ROOT}', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='pictures', default=None)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            related_name='pictures', default=None)

    def __str__(self):
        return self.image.url
