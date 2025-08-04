from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import UserRegisterForm




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    notices = Notice.objects.all()
    return render(request, 'main/profile.html', {
        'notices': notices,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })
from django.shortcuts import render, redirect

# Create your views here.
