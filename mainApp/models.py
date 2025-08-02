from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Місто", unique=True)

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
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_departures', verbose_name="З міста")
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_arrivals', verbose_name="У місто")
    departure_datetime = models.DateTimeField(verbose_name="Дата та час відправлення")
    arrival_datetime = models.DateTimeField(verbose_name="Дата та час прибуття")
    price_travel = models.DecimalField(verbose_name="Ціна поїздки", max_digits=10, decimal_places=2)
    from_place = models.CharField("Місце відправлення", max_length=250, default="Неизвестно")
    to_place = models.CharField("Місце прибуття", max_length=250, default="Неизвестно")


    def __str__(self):
        return (
            f"{self.from_city} → {self.to_city} "
            f"({self.departure_datetime:%d.%m %H:%M} - {self.arrival_datetime:%d.%m %H:%M}) "
            f"за ціною {self.price_travel} $"
        )


class Trip(models.Model):
    number_trip = models.PositiveIntegerField(verbose_name="Номер рейсу")
    carrier = models.CharField("Перевізник", max_length=250, default="Неизвестно")
    bus_description = models.CharField(
        max_length=255,
        default="Без опису",
        verbose_name="Опис автобуса"
    )
    count_passengers = models.PositiveIntegerField("Кількість місць", default=10)
    free_count_passengers = models.PositiveIntegerField("Вільні місця", default=10)

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



