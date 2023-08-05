from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
@api_view(['POST'])
# @permission_classes([HasAPIKey])
def chat(request):
    data = request.data
    # Get the "message" and "context" from the request body
    message = data['message']
    context = data['context']

    # Implement your logic for processing the message and context here
    # For simplicity, we'll just echo back the message and context
    new_message = f"Received message: {message}"

    return Response(new_message)