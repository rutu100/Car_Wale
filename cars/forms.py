from django import forms
from .models import Car, Comment, FuelType ,TestDrive
from django.utils import timezone


# =========================
# CAR FORM (ADMIN ADD / EDIT)
# =========================
class CarForm(forms.ModelForm):

    # 🔥 Multiple fuel types (Petrol, CNG, Electric etc.)
    fuel_types = forms.ModelMultipleChoiceField(
        queryset=FuelType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Fuel Types"
    )

    class Meta:
        model = Car
        fields = [
            'brand',
            'name',
            'description',
            'image',

            # 🔹 New specifications
            'model_year',
            'engine',
            'body_type',

            # 🔹 Pricing
            'price',
            'on_road_price',
            'quantity',

            # 🔹 Technical
            'fuel_types',
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

            'model_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 2024'
            }),

            'engine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 1.2L Petrol'
            }),

            'body_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex-showroom price'
            }),

            'on_road_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'On-road price'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
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
# COMMENT FORM
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


class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = [
            'name',
            'phone',
            'car',
            'preferred_date',
            'preferred_slot'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile number'
            }),

            'car': forms.Select(attrs={
                'class': 'form-control'
            }),

            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'preferred_slot': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    # ✅ 1️⃣ Disable past dates (BACKEND VALIDATION)
    def clean_preferred_date(self):
        date = self.cleaned_data.get('preferred_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError("Past dates are not allowed.")
        return date

    # ✅ 2️⃣ Disable already booked slots
    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get('car')
        date = cleaned_data.get('preferred_date')
        slot = cleaned_data.get('preferred_slot')

        if car and date and slot:
            already_booked = TestDrive.objects.filter(
                car=car,
                preferred_date=date,
                preferred_slot=slot,
                status__in=['Pending', 'Approved']
            ).exists()

            if already_booked:
                raise forms.ValidationError(
                    "This time slot is already booked. Please choose another slot."
                )

        return cleaned_data
