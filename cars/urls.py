from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cars, name='cars'),
    path('brand/<slug:brand_slug>/', views.cars, name='brand_wise_car'),
    path('post_car/', login_required(views.AddCar.as_view()), name="post_car"),
    path('edit/<int:id>/', login_required(views.EditPost.as_view()), name="edit_post"),
    path('delete/<int:id>/', login_required(views.DeletePost.as_view()), name="delete_post"),
    path('details/<int:id>/', views.CarDetails.as_view(), name="car_details"),
    path('buy/<int:id>/', views.buy_car, name="buy_car"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)