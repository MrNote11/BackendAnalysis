from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from drf_yasg import openapi
from rest_framework.generics import ListAPIView
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import logging
from decimal import Decimal 
logger = logging.getLogger(__name__)

# Create your views here.

class WelcomeMessageView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Welcome message endpoint to check API health.",
        responses={200: openapi.Response('Successful Response', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Welcome message'),
            }
        ))}
    )
    def get(self, request):
        """
        A simple welcome message endpoint to verify that the API is running.
        """
        return Response({"message": "Welcome to the YouTube Video Analytics API!"}, status=status.HTTP_200_OK)
    

def welcome_message(request):
    return HttpResponse("Welcome to the API, Built by Sulaiman😛")


class ReadEvent(APIView):
    def get(self, request, pk=None):
        if pk:
            return Response({"id": pk})
        
        else:
            return Response({"response": [1, 2, 3, 4]})
    