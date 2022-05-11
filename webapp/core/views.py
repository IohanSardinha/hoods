from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestSerializer

def front(request):
    context = { }
    return render(request, "index.html", context)


@api_view(['GET'])
def get_test(request):
    yourdata= {"responseCode": 200, "responseText": "It works!!!"}
    results = TestSerializer(yourdata).data
    return Response(results)
