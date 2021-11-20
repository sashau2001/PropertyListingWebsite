# Generated by Django 3.2.8 on 2021-11-16 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('apt_name', models.CharField(max_length=100)),
                ('apt_location', models.TextField()),
                ('apt_area', models.IntegerField(null=True)),
                ('apt_price', models.IntegerField(null=True)),
                ('apt_beds', models.IntegerField(null=True)),
                ('apt_baths', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('apt_lease', models.IntegerField(null=True)),
                ('apt_deposit', models.IntegerField(null=True)),
                ('apt_movein', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apt_reviewer', models.CharField(max_length=100)),
                ('apt_review', models.TextField()),
                ('apt_stars', models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')])),
                ('apt_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='b02_housing_app.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
