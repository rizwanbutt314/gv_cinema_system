# Generated by Django 3.0.7 on 2020-06-15 10:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Name of Genre', max_length=255)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Name of Language', max_length=255)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of Movie', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Description of Movie')),
                ('image_path', models.CharField(help_text='Image path of Movie', max_length=255)),
                ('duration', models.IntegerField(blank=True, help_text='Duration of Movie')),
                ('mpaa_rating', django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='JSON of the Mpaa Rating')),
                ('user_rating', models.CharField(blank=True, max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('genre', models.ManyToManyField(to='movies.Genre')),
                ('language', models.ForeignKey(help_text="Movie's language", null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Language')),
            ],
        ),
    ]
