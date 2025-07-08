from django.db import models


class Post(models.Model):
    objects = models.Manager()
    TYPE_CHOICES = {
        '1': "Sale",
        '2': "News",
        '3': "Text",
    }

    title = models.CharField(max_length=100, null=False, verbose_name='Заголовок')
    img = models.ImageField(null=False, upload_to='news/images', verbose_name='Фото')
    description = models.TextField(null=False, verbose_name='Описание')
    date = models.DateField(auto_created=True, null=True, verbose_name='Дата публикации')
    type = models.TextField(verbose_name='Тип', null=True, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title
