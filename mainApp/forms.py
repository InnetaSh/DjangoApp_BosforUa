from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['from_city', 'to_city', 'date_travel', 'count_passenger']
        widgets = {
            'date_travel': forms.DateInput(attrs={'type': 'date'}),
        }


