from django import forms
from .models import Ticket, Trip, TripRoute, Route, City
from django.forms import inlineformset_factory, formset_factory
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['from_city', 'to_city', 'date_travel', 'count_passenger']
        widgets = {
            'date_travel': forms.DateInput(attrs={'type': 'date'}),
        }


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ['carrier']
        fields = [
            'number_trip',
            'bus_description',
            'count_passengers',
            'free_count_passengers',
            'has_air_conditioning',
            'has_wifi',
            'has_paid_socket',
            'has_free_socket',
            'has_seat_belts',
            'has_wc',
            'has_eticket',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['from_city', 'to_city' , 'from_place', 'to_place', 'departure_datetime', 'arrival_datetime', 'price_travel']


class TripRouteWithRouteForm(forms.Form):
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), label="Отправление:")
    from_place = forms.CharField(max_length=250, label="Місце відправлення")

    to_city = forms.ModelChoiceField(queryset=City.objects.all(), label="Прибытие:")
    to_place = forms.CharField(max_length=250, label="Місце прибуття")

    departure_datetime = forms.DateTimeField(
        label="Время отправления",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    arrival_datetime = forms.DateTimeField(
        label="Время прибытия",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    price_travel = forms.DecimalField(max_digits=10, decimal_places=2, label="Цена")
    order = forms.IntegerField(label="Порядок")

TripRouteWithRouteFormSet = formset_factory(TripRouteWithRouteForm, extra=1, can_delete=False)