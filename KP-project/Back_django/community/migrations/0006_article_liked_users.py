# Generated by Django 4.2.16 on 2025-05-23 02:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0005_remove_article_genre_article_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='liked_users',
            field=models.ManyToManyField(blank=True, related_name='liked_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
