from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models

from .models import Car, Wishlist, Rating
from .forms import CarForm, CommentForm , TestDriveForm , TestDrive


# =====================================================
# HOME + SEARCH + FILTERS + SORTING
# =====================================================
def home(request):
    cars = Car.objects.all()

    # 🔍 Search by car name
    search = request.GET.get('search')
    if search:
        cars = cars.filter(name__icontains=search)

    # 💰 Max price filter
    max_price = request.GET.get('max_price')
    if max_price:
        cars = cars.filter(price__lte=max_price)

    # 🏷 Brand filter
    brand = request.GET.get('brand')
    if brand:
        cars = cars.filter(brand__name__iexact=brand)

    # ⛽ Fuel filter (ManyToMany)
    fuel = request.GET.get('fuel')
    if fuel:
        cars = cars.filter(fuel_types__name__iexact=fuel)

    # ⚙ Transmission filter
    transmission = request.GET.get('transmission')
    if transmission:
        cars = cars.filter(transmission__iexact=transmission)

    # 🔽 SORTING (✅ ADDED)
    sort = request.GET.get('sort')
    if sort == 'price_low':
        cars = cars.order_by('price')
    elif sort == 'price_high':
        cars = cars.order_by('-price')
    elif sort == 'rating':
        cars = cars.order_by('-rating')

    context = {
        'cars': cars
    }

    # ⚡ AJAX support
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'cars/car_list.html', context)

    return render(request, 'home.html', context)

# =====================================================
# ABOUT PAGE

def about(request):
    return render(request, 'about.html')





# =====================================================
# LIVE SEARCH SUGGESTIONS
# =====================================================
def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []

    if query:
        cars = Car.objects.filter(name__icontains=query)[:5]
        suggestions = [car.name for car in cars]

    return JsonResponse(suggestions, safe=False)


# =====================================================
# ADD CAR (ADMIN ONLY)
# =====================================================
@login_required
def add_cars(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admin can add cars.")
        return redirect('home')

    form = CarForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        car = form.save(commit=False)
        car.author = request.user
        car.save()
        form.save_m2m()  # REQUIRED for fuel_types
        messages.success(request, "Car added successfully!")
        return redirect('home')

    return render(request, 'form.html', {
        'form': form,
        'title': 'Add Car',
        'button_text': 'Add Car',
        'button_class': 'btn-success'
    })


# =====================================================
# CAR DETAIL PAGE
# =====================================================
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all()
    comment_form = CommentForm()

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            car=car
        ).exists()

    if request.method == 'POST':

        # 🛒 Buy Now
        if 'buy_now' in request.POST:
            if not request.user.is_authenticated:
                return redirect('login')

            if car.quantity > 0:
                car.quantity -= 1
                car.buyers.add(request.user)
                car.save()
                messages.success(request, "Car purchased successfully!")
            else:
                messages.error(request, "Car is out of stock.")

        # 💬 Add Comment
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.car = car
                comment.save()
                messages.success(request, "Comment added successfully!")

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'comments': comments,
        'comment_form': comment_form,
        'in_wishlist': in_wishlist
    })



def compare_cars(request):
    cars = Car.objects.all()

    car1_id = request.GET.get('car1')
    car2_id = request.GET.get('car2')

    car1 = Car.objects.filter(id=car1_id).first()
    car2 = Car.objects.filter(id=car2_id).first()

    return render(request, 'cars/compare.html', {
        'cars': cars,
        'car1': car1,
        'car2': car2,
    })


# =====================================================
# RATE CAR ⭐
# =====================================================
@login_required
def rate_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        value = int(request.POST.get('rating'))

        Rating.objects.update_or_create(
            car=car,
            user=request.user,
            defaults={'rating': value}
        )

        avg_rating = car.ratings.aggregate(
            avg=models.Avg('rating')
        )['avg']

        car.rating = round(avg_rating or 0, 1)
        car.save()

        messages.success(request, "Thanks for rating ⭐")

    return redirect('car_detail', car_id=car.id)


# =====================================================
# WISHLIST
# =====================================================
@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Wishlist.objects.get_or_create(
        user=request.user,
        car=car
    )
    messages.success(request, "Added to wishlist ❤️")
    return redirect('car_detail', car_id=car.id)


@login_required
def remove_from_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Wishlist.objects.filter(
        user=request.user,
        car=car
    ).delete()
    messages.success(request, "Removed from wishlist ❌")
    return redirect('wishlist')


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'cars/wishlist.html', {'items': items})


# =====================================================
# EDIT / DELETE CAR (ADMIN ONLY)
# =====================================================
@login_required
def edit_car(request, car_id):
    if not request.user.is_superuser:
        messages.error(request, "Only admin can edit cars.")
        return redirect('home')

    car = get_object_or_404(Car, id=car_id)
    form = CarForm(request.POST or None, request.FILES or None, instance=car)

    if form.is_valid():
        form.save()
        messages.success(request, "Car updated successfully!")
        return redirect('car_detail', car_id=car.id)

    return render(request, 'form.html', {
        'form': form,
        'title': 'Edit Car',
        'button_text': 'Update Car',
        'button_class': 'btn-warning'
    })


@login_required
def delete_car(request, car_id):
    if not request.user.is_superuser:
        messages.error(request, "Only admin can delete cars.")
        return redirect('home')

    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, "Car deleted successfully!")
    return redirect('home')



@login_required
def test_drive(request):
    form = TestDriveForm(
    request.POST or None,
    initial={'car': request.GET.get('car')}
    )


    if form.is_valid():
        test_drive = form.save(commit=False)
        test_drive.user = request.user
        test_drive.save()
        messages.success(request, "Test drive booked successfully 🚗")
        return redirect('home')

    return render(request, 'form.html', {
        'form': form,
        'title': 'Book Test Drive',
        'button_text': 'Book Test Drive',
        'button_class': 'btn-success'
    })

@login_required
def my_test_drives(request):
    drives = TestDrive.objects.filter(user=request.user)
    return render(request, 'cars/my_test_drives.html', {
        'drives': drives
    })


@login_required
def cancel_test_drive(request, drive_id):
    drive = TestDrive.objects.get(id=drive_id, user=request.user)

    if drive.status == 'Pending':
        drive.status = 'Cancelled'
        drive.save()
        messages.success(request, "Test drive cancelled successfully.")
    else:
        messages.error(request, "Only pending test drives can be cancelled.")

    return redirect('my_test_drives')
