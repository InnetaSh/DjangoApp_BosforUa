from django.core.management.base import BaseCommand
from mainApp.models import City, Station

class Command(BaseCommand):
    help = 'Завантажує список міст та зупинок до кожного міста'

    def handle(self, *args, **kwargs):
        data = {
            'Київ': ['Центральний автовокзал', 'ЖД Вокзал', 'Автостанція Південна'],
            'Львів': ['Львівський автовокзал', 'Площа Двірцева'],
            'Дніпро': ['Центральна автостанція', 'Вокзал'],
            'Одеса': ['Автовокзал Привоз', 'ЖД Вокзал'],
            'Харків': ['Центральний вокзал', 'Автостанція №2'],
            'Миколаїв': ['Автовокзал', 'ЖД Вокзал'],
            'Полтава': ['Автостанція Київська', 'Центральний вокзал'],
            'Запоріжжя': ['Автостанція-1', 'ЖД Вокзал Запоріжжя-1'],
            'Херсон': ['Автостанція Центральна', 'ЖД Вокзал'],
            'Черкаси': ['Автовокзал', 'ЖД Вокзал'],
            'Чернігів': ['Автостанція №1', 'ЖД Вокзал'],
            'Суми': ['Автостанція Центральна', 'ЖД Вокзал'],
            'Житомир': ['Центральний автовокзал', 'ЖД Вокзал'],
            'Рівне': ['Автостанція Центральна'],
            'Івано-Франківськ': ['Автостанція №2', 'ЖД Вокзал'],
            'Тернопіль': ['Автовокзал', 'Площа Привокзальна'],
            'Ужгород': ['Автовокзал', 'ЖД Вокзал'],
            'Кропивницький': ['Центральний автовокзал'],
            'Луцьк': ['Автостанція', 'Вокзал'],
            'Чернівці': ['Автовокзал Центральний', 'Вокзал'],
            'Донецьк': ['Автовокзал "Южный"'],
            'Луганськ': ['Автостанція Центральна'],
            'Кривий Ріг': ['ЖД Вокзал', 'Автостанція Південна'],
            'Сімферополь': ['Автовокзал', 'ЖД Вокзал'],
            'Хмельницький': ['Центральний автовокзал'],
            'Вінниця': ['Автовокзал "Західний"', 'Центральний залізничний вокзал'],
        }

        total_created_cities = 0
        total_created_stations = 0

        for city_name, station_names in data.items():
            city, city_created = City.objects.get_or_create(name=city_name)
            if city_created:
                self.stdout.write(self.style.SUCCESS(f"🟢 Створено місто: {city_name}"))
                total_created_cities += 1
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Місто вже існує: {city_name}"))

            for station_name in station_names:
                station, created = Station.objects.get_or_create(name=station_name, city=city)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"   └ Зупинка: {station_name}"))
                    total_created_stations += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Завершено: створено міст: {total_created_cities}, зупинок: {total_created_stations}"
        ))
