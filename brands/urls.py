from django.urls import path
from . import views

urlpatterns = [
    path('add_brand/', views.add_brand, name="add_brand")
]
