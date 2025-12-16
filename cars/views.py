from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Car, Comment
from .forms import CarForm, CommentForm


# ================= ADD CAR =================
@login_required
def add_cars(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.author = request.user
            car.save()
            messages.success(request, 'Car added successfully!')
            return redirect('home')
    else:
        form = CarForm()

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

    if request.method == 'POST':

        # BUY NOW
        if 'buy_now' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to buy this car.')
                return redirect('login')

            if car.quantity > 0:
                car.buyers.add(request.user)
                car.quantity -= 1
                car.save()
                messages.success(request, 'Car purchased successfully!')
            else:
                messages.error(request, 'Car is out of stock.')

        # ADD COMMENT
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.car = car
                new_comment.save()
                messages.success(request, 'Comment added successfully!')

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'comments': comments,
        'comment_form': comment_form
    })
