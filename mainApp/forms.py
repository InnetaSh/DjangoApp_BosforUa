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
        fields = ['number_trip']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['from_city', 'to_city', 'departure_datetime', 'arrival_datetime', 'price_travel']



class TripRouteWithRouteForm(forms.ModelForm):
    order = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Route
        fields = ['from_city', 'to_city', 'departure_datetime', 'arrival_datetime', 'price_travel']
        widgets = {
            'departure_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

TripRouteWithRouteFormSet = formset_factory(TripRouteWithRouteForm, extra=1, can_delete=True)