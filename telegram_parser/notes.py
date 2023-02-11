# flake8: noqa

Модель "News" может выглядеть следующим образом в проекте Django:

python
Copy code
from django.db import models

class News(models.Model):
    source = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    attachments = models.ManyToManyField(Picture)
    
    def __str__(self):
        return self.source
Здесь используются следующие поля:

source - источник новости (яндекс, ozon), тип поля - CharField
time - время публикации, тип поля - DateTimeField
tags - тэги, связь с моделью Tag, тип поля - ManyToManyField
content - текст новости, тип поля - TextField
attachments - вложения (картинки), связь с моделью Picture, тип поля - ManyToManyField
Функция __str__ возвращает строковое представление модели, в данном случае - источник новости.