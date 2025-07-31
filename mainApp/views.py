
from django.shortcuts import render, redirect
from .models import City, Ticket, Trip, Route, TripRoute
from .forms import TicketForm,  RouteForm, TripForm, TripRouteWithRouteFormSet


from .context_data import (
    features, about, routes_blocks,
    footer_blocks, footer_blocks_img
)




def home(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()


    return render(request, 'mainApp/home.html', {
        'form': form,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img':footer_blocks_img
    })


def create_trip_view(request):
    if request.method == 'POST':
        trip_form = TripForm(request.POST)
        formset = TripRouteWithRouteFormSet(request.POST)

        if trip_form.is_valid() and formset.is_valid():
            trip = trip_form.save()

            for form in formset:
                if not form.cleaned_data:
                    continue
                data = form.cleaned_data
                route = Route.objects.create(
                    from_city=data['from_city'],
                    to_city=data['to_city'],
                    departure_datetime=data['departure_datetime'],
                    arrival_datetime=data['arrival_datetime'],
                    price_travel=data['price_travel'],
                )
                TripRoute.objects.create(
                    trip=trip,
                    route=route,
                    order=data['order'],
                )

            return redirect('success_url')

    else:
        trip_form = TripForm()
        formset = TripRouteWithRouteFormSet()

    return render(request, 'mainApp/add_trip.html', {
        'trip_form': trip_form,
        'formset': formset,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img': footer_blocks_img
    })

