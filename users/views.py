from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.parse import urlencode

from mainApp.forms import TicketForm
from .form import UserRegisterForm, CarrierRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from mainApp.context_data import (
    features, about, routes_blocks,
    footer_blocks, footer_blocks_img
)


def register_carrier(request):
    if request.method == 'POST':
        form = CarrierRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Реєстрація перевізника пройшла успішно!')
            return redirect('create_trip')
    else:
        form = CarrierRegisterForm()
    return render(request, 'users/register_carrier.html', {'form': form})



@login_required
def profile_carrier(request):

    return redirect('create_trip')


@login_required
def profile(request):
    if request.method == 'POST':
        search_form_top = TicketForm(request.POST, prefix='form-top')
        form = TicketForm(request.POST)
        if form.is_valid() or search_form_top.is_valid():
            query_string = urlencode({
                'from_city': form.cleaned_data['from_city'].id,
                'to_city': form.cleaned_data['to_city'].id,
                'date_travel': form.cleaned_data['date_travel'].isoformat(),
                'count_passenger': form.cleaned_data['count_passenger']
            })

            search_url = f"{reverse('search_tickets')}?{query_string}"
            return redirect(search_url)
    else:
        form = TicketForm()
        search_form_top = TicketForm(prefix='form-top')

    return render(request, 'mainApp/profile.html', {
        'form': form,
        'search_form_top': search_form_top,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img': footer_blocks_img
    })




def logout(request):
    auth_logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})





