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
