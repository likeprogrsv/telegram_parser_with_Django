# Generated by Django 4.1.6 on 2023-02-12 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_news', '0004_alter_picture_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(null=True, upload_to='C:\\Storage\\Programming\\Repo_GIT\\telegram_parser_with_Django\\telegram_parser/static/'),
        ),
    ]
