from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    isCarrier = models.BooleanField(default=False, verbose_name="Перевізник")

    company_name = models.CharField("Назва компанії", max_length=150, blank=True, null=True)
    contact_person = models.CharField("Контактна особа", max_length=150, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username if not self.isCarrier else f"{self.company_name or self.username}"
