from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class CarrierLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Назва компанії",
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class CarrierRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'contact_person', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Меняем подпись поля username на "Назва компанії"
        self.fields['username'].label = "Назва компанії"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.isCarrier = True
        # Дублируем значение username в company_name
        user.company_name = self.cleaned_data.get("username")
        if commit:
            user.save()
        return user