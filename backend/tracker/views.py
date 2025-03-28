from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    response = render(request, "tracker/index.html", {})
    return response