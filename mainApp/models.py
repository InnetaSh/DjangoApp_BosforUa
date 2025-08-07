from django.db import models
from django.conf import settings

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Місто", unique=True)

    def __str__(self):
        return self.name



class Station(models.Model):
    name = models.CharField(max_length=100, verbose_name="Станція")  # Убрал unique=True
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='stations', verbose_name="Місто")

    class Meta:
        unique_together = ('city', 'name')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ticket_departures', verbose_name="З міста")
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ticket_arrivals', verbose_name="У місто")
    date_travel = models.DateField(verbose_name="Дата поїздки")
    count_passenger = models.PositiveIntegerField(verbose_name="Кількість пасажирів")

    def __str__(self):
        return f"{self.from_city} → {self.to_city} на {self.date_travel} ({self.count_passenger} пасажирів)"



class Route(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_departures',
                                  verbose_name="З міста")
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_arrivals', verbose_name="У місто")

    from_place = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='routes_from',
                                   verbose_name="Зупинка відправлення")
    to_place = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='routes_to',
                                 verbose_name="Зупинка прибуття")

    departure_datetime = models.DateTimeField(verbose_name="Дата та час відправлення")
    arrival_datetime = models.DateTimeField(verbose_name="Дата та час прибуття")
    price_travel = models.DecimalField(verbose_name="Ціна поїздки", max_digits=10, decimal_places=2)



    def __str__(self):
        return (
            f"{self.from_city} {self.from_place}→ {self.to_city} {self.to_place}"
            f"({self.departure_datetime:%d.%m %H:%M} - {self.arrival_datetime:%d.%m %H:%M}) "
            f"за ціною {self.price_travel} $"
        )


class Trip(models.Model):
    number_trip = models.PositiveIntegerField(verbose_name="Номер рейсу")
    carrier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trips',
        verbose_name="Перевізник",
        limit_choices_to={'isCarrier': True}
    )

    bus_description = models.CharField(
        max_length=255,
        default="Без опису",
        verbose_name="Опис автобуса"
    )
    count_passengers = models.PositiveIntegerField("Кількість місць", default=10)
    free_count_passengers = models.PositiveIntegerField("Вільні місця", default=10)

    has_air_conditioning = models.BooleanField("Кондиціонер", default=False)
    has_wifi = models.BooleanField("Wi-Fi", default=False)
    has_paid_socket = models.BooleanField("Розетка (платно)", default=False)
    has_free_socket = models.BooleanField("Розетка (безкоштовно)", default=False)
    has_seat_belts = models.BooleanField("Ремені безпеки", default=False)
    has_wc = models.BooleanField("WC", default=False)

    has_eticket = models.BooleanField("Без роздруковування", default=False)

    def __str__(self):
        return f"Рейс №{self.number_trip}"

    def get_ordered_routes(self):
        return [tr.route for tr in self.trip_routes.order_by('order')]

    def is_valid_route_sequence(self):
        ordered = self.get_ordered_routes()
        for i in range(len(ordered) - 1):
            if ordered[i].to_city != ordered[i + 1].from_city:
                return False
        return True


class TripRoute(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_routes')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.trip} – {self.route} (#{self.order})"





