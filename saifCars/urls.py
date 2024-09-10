
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls')),
    path('authors/', include('authors.urls')),
    path('brands/', include('brands.urls')),
]
 