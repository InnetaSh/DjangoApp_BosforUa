
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
    print("➡ POST данные:")
    for key, value in request.POST.items():
        print(f"{key}: {value}")

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
                    continue  # форма пустая, не трогаем

                if not form.is_valid():
                    print(f"Форма #{i} невалидна: {form.errors}")
                    continue

                # тут уже можно использовать cleaned_data
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

            return redirect('success_url')

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
