from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Місто", unique=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departures', verbose_name="З міста")
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrivals', verbose_name="У місто")
    date_travel = models.DateField(verbose_name="Дата поїздки")
    count_passenger = models.PositiveIntegerField(verbose_name="Кількість пасажирів")

    def __str__(self):
        return f"{self.from_city} → {self.to_city} на {self.date_travel} ({self.count_passenger} пасажирів)"
