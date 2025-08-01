from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.urls import reverse

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

    return render(request, 'mainApp/home.html', {
        'form': form,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img': footer_blocks_img
    })


def search_tickets(request):
    form = TicketForm(request.GET or None)
    found_trips = []

    if form.is_valid():
        from_city = form.cleaned_data['from_city']
        to_city = form.cleaned_data['to_city']
        date_travel = form.cleaned_data['date_travel']
        count_passenger = form.cleaned_data['count_passenger']

        all_trips = Trip.objects.filter(free_count_passengers__gte=count_passenger)

        for trip in all_trips:
            routes = list(trip.trip_routes.select_related('route').order_by('order'))

            from_index, to_index = None, None
            for i, tr in enumerate(routes):
                for i, tr in enumerate(routes):
                    print(f"Checking route {i}: order={tr.order} from {tr.route.from_city} to {tr.route.to_city}")

                    if from_index is None:
                        if tr.route.from_city == from_city and tr.route.departure_datetime.date() == date_travel:
                            from_index = i
                            print(f"Found from_index at index {i}, order {tr.order}")
                    else:
                        if tr.route.to_city == to_city and tr.order >= routes[from_index].order:
                            to_index = i
                            print(f"Found to_index at index {i}, order {tr.order}")
                            break

            if from_index is not None and to_index is not None and from_index <= to_index:
                found_trips.append(trip)
    return render(request, 'mainApp/search_tickets.html', {
        'form': form,
        'trips': found_trips,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img': footer_blocks_img
    })

def create_trip_view(request):
    if request.method == 'POST':
        trip_form = TripForm(request.POST)
        formset = TripRouteWithRouteFormSet(request.POST)

        print("➡ POST данные:")
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        if trip_form.is_valid() and formset.is_valid():
            trip = trip_form.save()

            for i, form in enumerate(formset):
                if not form.has_changed():
                    continue

                if not form.is_valid():
                    print(f"Форма #{i} невалидна: {form.errors}")
                    continue

                route = Route.objects.create(
                    from_city=form.cleaned_data['from_city'],
                    to_city=form.cleaned_data['to_city'],
                    departure_datetime=form.cleaned_data['departure_datetime'],
                    arrival_datetime=form.cleaned_data['arrival_datetime'],
                    price_travel=form.cleaned_data['price_travel'],
                )

                TripRoute.objects.create(
                    trip=trip,
                    route=route,
                    order=form.cleaned_data['order']
                )

            return redirect('home')

        else:
            print("❌ Ошибки в TripForm:", trip_form.errors.as_data())
            print("❌ Ошибки в Formset:")

            for i, form in enumerate(formset):
                print(f"Форма #{i}:")
                print(form.errors.as_data())

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
