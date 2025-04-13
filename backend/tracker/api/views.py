from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



@api_view(['GET'])
def index(request: HttpRequest) -> HttpResponse:
    return Response('Rest Framework setup ok.')