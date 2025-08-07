from urllib.parse import urlencode

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import City, Ticket, Trip, Route, TripRoute, Station
from .forms import TicketForm,  RouteForm, TripForm, TripRouteWithRouteFormSet
from datetime import timedelta

from .context_data import (
    features, about, routes_blocks,
    footer_blocks, footer_blocks_img
)




def home(request):
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

    return render(request, 'mainApp/home.html', {
        'form': form,
        'search_form_top': search_form_top,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img': footer_blocks_img
    })


def format_duration(duration):
    total_minutes = int(duration.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours} год. {minutes} хв"

def search_tickets(request):
    form = TicketForm(request.GET or None)
    found_trips = []
    from_city=''
    to_city = ''
    date_travel =''

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
                segment_routes = []
                for r in routes[from_index:to_index + 1]:
                    if r.route.arrival_datetime >= r.route.departure_datetime:
                        duration = r.route.arrival_datetime - r.route.departure_datetime
                    else:
                        duration = (r.route.arrival_datetime + timedelta(days=1)) - r.route.departure_datetime
                    segment_routes.append({
                        'route': r.route,
                         'duration': format_duration(duration)
                    })
                found_trips.append({
                    'trip': trip,
                    'routes': segment_routes
                })
    return render(request, 'mainApp/search_tickets.html', {
        'form': form,
        'trips': found_trips,
        'to_city':to_city,
        'from_city':from_city,
        'date_travel':date_travel,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img': footer_blocks_img
    })



def get_stations(request):
    city_id = request.GET.get('city_id')
    stations_qs = Station.objects.filter(city_id=city_id)
    stations = [{"id": s.id, "name": s.name} for s in stations_qs]
    return JsonResponse({"stations": stations})




def get_city_options():
    return ''.join([f'<option value="{c.id}">{c.name}</option>' for c in City.objects.all()])

def carrier_trips(request):
    if not request.user.isCarrier:
        return redirect('home')


    carrier_trips = Trip.objects.filter(carrier=request.user)
    found_trips = []
    for trip in carrier_trips:
        found_trips.append({
            'trip': trip,
            'routes': trip.get_ordered_routes()
        })


    return render(request, 'mainApp/carrier_trips.html', {
        'carrier_trips': found_trips,
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


        if trip_form.is_valid() and formset.is_valid():
            trip = trip_form.save(commit=False)
            trip.carrier = request.user
            trip.save()

            for i, form in enumerate(formset):
                if not form.has_changed():
                    continue

                if not form.is_valid():
                    print(f"Форма #{i} невалидна: {form.errors}")
                    continue

                route = Route.objects.create(
                    from_city=form.cleaned_data['from_city'],
                    to_city=form.cleaned_data['to_city'],
                    from_place=form.cleaned_data['from_place'],
                    to_place=form.cleaned_data['to_place'],
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

        for i, form in enumerate(formset.forms):
            if 'from_city' in form.fields:
                current_classes = form.fields['from_city'].widget.attrs.get('class', '')
                new_classes = f"{current_classes} from-city from-city-{i}".strip()
                form.fields['from_city'].widget.attrs['class'] = new_classes

            if 'to_city' in form.fields:
                current_classes = form.fields['to_city'].widget.attrs.get('class', '')
                new_classes = f"{current_classes} to-city to-city-{i}".strip()
                form.fields['to_city'].widget.attrs['class'] = new_classes

    return render(request, 'mainApp/add_trip.html', {
        'trip_form': trip_form,
        'formset': formset,
        'features': features,
        'about': about,
        'routes_blocks': routes_blocks,
        'footer_blocks': footer_blocks,
        'footer_blocks_img': footer_blocks_img
    })
