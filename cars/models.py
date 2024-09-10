from django.db import models
from brands.models import Brand
from django.contrib.auth.models import User

# Create your models here.
class PostCar(models.Model):
    car_name = models.CharField(max_length=100)
    price = models.IntegerField()
    details = models.TextField()
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.car_name}"

class Comment(models.Model):
    post = models.ForeignKey(PostCar, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.name}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(PostCar, on_delete=models.CASCADE)
