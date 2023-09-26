from django.shortcuts import render

# Create your views here.
from rest_framework import generics

def apimodel(request):

    return render(request,'home.html')