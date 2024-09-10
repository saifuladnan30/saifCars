from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = forms.BrandForm(request.POST)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.slug = slugify(brand.brand_name)
            brand.save()
            messages.success(request, 'Brand added Successfully')
            return redirect(add_brand)
    else:
        form = forms.BrandForm()
    return render(request, 'brand.html', {'form': form})
 