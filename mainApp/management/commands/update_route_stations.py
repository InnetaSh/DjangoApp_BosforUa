# mainApp/management/commands/update_route_stations.py

from django.core.management.base import BaseCommand
from mainApp.models import Route, Station, City

class Command(BaseCommand):
    help = 'Обновить поля from_place и to_place у Route, сопоставив их с объектами Station'

    def handle(self, *args, **kwargs):
        routes = Route.objects.all()
        updated_count = 0
        skipped_count = 0

        for route in routes:
            # Предположим, что у тебя сейчас есть старые поля from_place_name, to_place_name
            # Или каким-то образом получаем названия остановок в виде строк
            from_place_name = getattr(route, 'from_place_name', None)
            to_place_name = getattr(route, 'to_place_name', None)

            # Если у тебя старые поля не существуют, замени логику извлечения названий
            if not from_place_name or not to_place_name:
                self.stdout.write(f"Пропускаем маршрут {route.id} — нет названий остановок")
                skipped_count += 1
                continue

            # Ищем станции по имени и городу (можно добавить фильтрацию по городу)
            try:
                from_station = Station.objects.get(name=from_place_name, city=route.from_city)
                to_station = Station.objects.get(name=to_place_name, city=route.to_city)
            except Station.DoesNotExist as e:
                self.stdout.write(f"Ошибка: {e} для маршрута {route.id}")
                skipped_count += 1
                continue

            route.from_place = from_station
            route.to_place = to_station
            route.save()
            updated_count += 1
            self.stdout.write(f"Обновлено маршрут {route.id}: {from_station} → {to_station}")

        self.stdout.write(self.style.SUCCESS(
            f"Обновление завершено. Обновлено: {updated_count}, пропущено: {skipped_count}"
        ))
