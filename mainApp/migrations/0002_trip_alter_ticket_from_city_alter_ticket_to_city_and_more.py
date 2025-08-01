# Generated by Django 5.2.4 on 2025-07-31 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_trip', models.PositiveIntegerField(verbose_name='Номер рейсу')),
            ],
        ),
        migrations.AlterField(
            model_name='ticket',
            name='from_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_departures', to='mainApp.city', verbose_name='З міста'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='to_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_arrivals', to='mainApp.city', verbose_name='У місто'),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_datetime', models.DateTimeField(verbose_name='Дата та час відправлення')),
                ('arrival_datetime', models.DateTimeField(verbose_name='Дата та час прибуття')),
                ('price_travel', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна поїздки')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_departures', to='mainApp.city', verbose_name='З міста')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_arrivals', to='mainApp.city', verbose_name='У місто')),
            ],
        ),
        migrations.CreateModel(
            name='TripRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.route')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_routes', to='mainApp.trip')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
