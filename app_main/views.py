from django.shortcuts import render
from django.views.generic import ListView
from app_product import models


# class HomeViews(ListView):
#     model = models.Category
#     template_name = 'app_product/categories.html'
#     context_object_name = 'home'