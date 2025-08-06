from django.core.management.base import BaseCommand
from mainApp.models import City

class Command(BaseCommand):
    help = 'Завантажує список міст в базу даних'

    def handle(self, *args, **kwargs):
        cities = [
            'Вінниця', 'Дніпро', 'Донецьк', 'Житомир', 'Запоріжжя',
            'Івано-Франківськ', 'Київ', 'Кропивницький', 'Кривий Ріг', 'Луганськ',
            'Луцьк', 'Львів', 'Миколаїв', 'Одеса', 'Полтава', 'Рівне', 'Суми',
            'Тернопіль', 'Ужгород', 'Харків', 'Херсон', 'Хмельницький', 'Черкаси',
            'Чернівці', 'Чернігів', 'Сімферополь',
        ]

        for name in cities:
            city, created = City.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS(
                f"{'Створено' if created else 'Вже є'}: {name}"
            ))