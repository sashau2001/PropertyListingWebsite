# Generated by Django 3.2.8 on 2021-10-26 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b02_housing_app', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='apt_stars',
            field=models.IntegerField(default=5),
        ),
    ]
