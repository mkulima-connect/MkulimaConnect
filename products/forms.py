from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "location", "category", "quantity"]
        labels = {
            "name": "Product Name",
            "price": "Price (TZS)",
            "image": "Crop Image",
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_quantity(self):
        qty = self.cleaned_data["quantity"]
        if qty < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return qty


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} ★") for i in range(1, 6)]
    COMMENT_CHOICES = [
        ("Very Poor", "Very Poor"),
        ("Poor", "Poor"),
        ("Satisfied", "Satisfied"),
        ("Good", "Good"),
        ("Best", "Best"),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    comment = forms.ChoiceField(choices=COMMENT_CHOICES, widget=forms.Select)

    class Meta:
        model = Review
        fields = ["rating", "comment"]
