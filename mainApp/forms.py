from django import forms
from .models import Ticket, Trip, TripRoute, Route, City
from django.forms import inlineformset_factory, formset_factory


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
        fields = ['number_trip', 'carrier', 'bus_description', 'count_passengers']


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['from_city', 'to_city', 'departure_datetime', 'arrival_datetime', 'price_travel']


class TripRouteWithRouteForm(forms.Form):
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), label="Отправление:")
    to_city = forms.ModelChoiceField(queryset=City.objects.all(), label="Прибытие:")
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