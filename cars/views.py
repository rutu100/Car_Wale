from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Rating
from django.db import models


from .models import Car, Comment, Wishlist
from .forms import CarForm, CommentForm


# ================= HOME + SEARCH + FILTERS =================
def home(request):
    cars = Car.objects.all()

    # 🔍 SEARCH BY NAME
    search = request.GET.get('search')
    if search:
        cars = cars.filter(name__icontains=search)

    # 💰 PRICE FILTER (Slider)
    max_price = request.GET.get('max_price')
    if max_price:
        cars = cars.filter(price__lte=max_price)

    # 🏷 BRAND FILTER (Only TATA)
    brand = request.GET.get('brand')
    if brand:
        cars = cars.filter(brand__name__iexact=brand)

    context = {
        'cars': cars
    }

    # ⚡ AJAX SUPPORT (no page reload)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'cars/car_list.html', context)

    return render(request, 'home.html', context)


# ================= LIVE SEARCH SUGGESTIONS =================
def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []

    if query:
        cars = Car.objects.filter(name__icontains=query)[:5]
        suggestions = [car.name for car in cars]

    return JsonResponse(suggestions, safe=False)


# ================= ADD CAR =================
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
        messages.success(request, "Car added successfully!")
        return redirect('home')

    return render(request, 'form.html', {
        'form': form,
        'title': 'Add Car',
        'button_text': 'Add Car',
        'button_class': 'btn-success'
    })


# ================= CAR DETAIL =================
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

        # 🛒 BUY NOW
        if 'buy_now' in request.POST:
            if not request.user.is_authenticated:
                return redirect('login')

            if car.quantity > 0:
                car.quantity -= 1
                car.buyers.add(request.user)
                car.save()
                messages.success(request, 'Car purchased successfully!')
            else:
                messages.error(request, 'Car is out of stock.')

        # 💬 ADD COMMENT
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.car = car
                comment.save()
                messages.success(request, 'Comment added successfully!')

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'comments': comments,
        'comment_form': comment_form,
        'in_wishlist': in_wishlist
    })


# ================= ADD TO WISHLIST =================
@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Wishlist.objects.get_or_create(
        user=request.user,
        car=car
    )
    messages.success(request, 'Added to wishlist ❤️')
    return redirect('car_detail', car_id=car.id)


# ================= REMOVE FROM WISHLIST =================
@login_required
def remove_from_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Wishlist.objects.filter(
        user=request.user,
        car=car
    ).delete()
    messages.success(request, 'Removed from wishlist ❌')
    return redirect('wishlist')


# ================= WISHLIST PAGE =================
@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'cars/wishlist.html', {
        'items': items
    })


# ================= EDIT CAR =================
@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if not (request.user == car.author or request.user.is_superuser):
        messages.error(request, "You are not allowed to edit this car.")
        return redirect('car_detail', car_id=car.id)

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


# ================= DELETE CAR =================
@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if not (request.user == car.author or request.user.is_superuser):
        messages.error(request, "You are not allowed to delete this car.")
        return redirect('car_detail', car_id=car.id)

    car.delete()
    messages.success(request, "Car deleted successfully!")
    return redirect('home')
# ================= RATE CAR =================
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

        # 🔄 Update average rating
        avg = car.ratings.aggregate(models.Avg('rating'))['rating__avg']
        car.rating = round(avg, 1)
        car.save()

        messages.success(request, "Thanks for rating ⭐")

    return redirect('car_detail', car_id=car.id)
