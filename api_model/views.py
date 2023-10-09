from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponseBadRequest
from api_model.models import ModelTemplate
from django.shortcuts import render
from django.template import Context, Template

def apimodel(request):

    return render(request,'home.html')


