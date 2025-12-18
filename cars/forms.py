from django import forms
from .models import Car, Comment


# =========================
# CAR FORM (ADMIN ADD / EDIT)
# =========================
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand',
            'name',
            'description',
            'image',
            'price',
            'quantity',

            # 🔹 NEW SPECIFICATIONS (ADMIN CONTROLLED)
            'fuel_type',
            'transmission',
            'mileage',
            'seating',
        ]

        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter car name'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter car description'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),

            # 🔧 SPECIFICATIONS
            'fuel_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'transmission': forms.Select(attrs={
                'class': 'form-control'
            }),

            'mileage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 20 km/l'
            }),

            'seating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 5'
            }),
        }


# =========================
# COMMENT FORM (UNCHANGED)
# =========================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            }),

            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }
