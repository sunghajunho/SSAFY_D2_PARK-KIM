# Generated by Django 4.2.16 on 2025-05-22 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('overview', models.TextField()),
                ('poster_path', models.CharField(max_length=300)),
                ('release_date', models.DateField(null=True)),
                ('vote_average', models.FloatField()),
                ('runtime', models.PositiveIntegerField(null=True)),
                ('adult', models.BooleanField()),
                ('original_language', models.CharField(max_length=10)),
                ('genres', models.ManyToManyField(related_name='movies_genre', to='core.genre')),
            ],
        ),
    ]
