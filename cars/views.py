from django.shortcuts import render, redirect
from . import forms
from . import models
from .forms import PostCarForm
from brands.models import Brand
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy
from .models import Brand, PostCar, Purchase
from django.contrib import messages

# Create your views here.


def cars(request, brand_slug=None):
    data = PostCar.objects.all()
    brands = Brand.objects.all()

    if brand_slug is not None:
        brand = Brand.objects.get(slug=brand_slug)
        data = PostCar.objects.filter(brand=brand)

    return render(request, 'cars.html', {'data': data, 'brands': brands})


class AddCar(CreateView):
    model = models.PostCar
    form_class = PostCarForm
    template_name = 'post_car.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class EditPost(UpdateView):
    model = models.PostCar
    form_class = forms.PostCarForm
    template_name = 'post_car.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

class DeletePost(DeleteView):
    model = models.PostCar
    template_name = 'delete_confirm.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

class CarDetails(DetailView):
    model = models.PostCar
    pk_url_kwarg = 'id'
    template_name = 'car_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentsForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return redirect('car_details', id=post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        comment_form = forms.CommentsForm()

        context['post'] = post
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

@login_required
def buy_car(request, id):
    try:
        car = PostCar.objects.get(pk=id, quantity_available__gt=0)
    except PostCar.DoesNotExist:
        messages.error(request, 'Car not found or no quantity available.')
        return redirect('cars')
    car.quantity_available -= 1
    car.save()
    Purchase.objects.create(user=request.user, car=car)
    messages.success(request, 'Car purchased successfully.')
    return redirect('profile')