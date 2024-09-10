from django import forms
from .models import PostCar, Comment

class PostCarForm(forms.ModelForm):
    class Meta:
        model = PostCar
        fields = ['car_name', 'price', 'details', 'brand', 'image', 'quantity_available']

        
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']