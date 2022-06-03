from django.shortcuts import render, reverse, redirect
from django.views import generic


# Create your views here.



class HomeView(generic.TemplateView):
    template_name = 'home.html'