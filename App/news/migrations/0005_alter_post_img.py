# Generated by Django 5.1 on 2024-09-01 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_remove_post_category_delete_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(upload_to='news/images', verbose_name='Фото'),
        ),
    ]
