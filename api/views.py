from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import api_view, permission_classes
from .pinecone_utils import PineconeUtils

# Create your views here.
@api_view(['POST'])
# @permission_classes([HasAPIKey])
def chat(request):
    headers = request.headers
    namespace = request.headers['namespace']
    api_key = request.headers['Api-Key']
    data = request.data
    # Get the "message" and "context" from the request body
    message = data['message']
    context = data['context']

    # Create a new pinecone_utils object to generate a new message using the context
    pinecone_utils = PineconeUtils(namespace=namespace, context=context)
    # Answers will be pulled from pincecone vector store with associated namespace
    reply = pinecone_utils.get_reply(message)
    return Response(reply)