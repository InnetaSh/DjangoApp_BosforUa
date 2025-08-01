# Generated by Django 5.2.4 on 2025-08-01 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_trip_alter_ticket_from_city_alter_ticket_to_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='bus_description',
            field=models.CharField(default='Без опису', max_length=255, verbose_name='Опис автобуса'),
        ),
        migrations.AddField(
            model_name='trip',
            name='carrier',
            field=models.CharField(default='Неизвестно', max_length=250, verbose_name='Перевізник'),
        ),
        migrations.AddField(
            model_name='trip',
            name='count_passengers',
            field=models.PositiveIntegerField(default=10, verbose_name='Кількість місць'),
        ),
    ]
