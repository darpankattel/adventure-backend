# AdVenture Django Backend

## Overview
This document provides a comprehensive guide for developing the Django backend for the AdVenture project. It includes features, dependencies, app structures, models, APIs, routing, and integration with AWS services.

## Table of Contents
1. [Features](#features)
2. [Django Apps](#django-apps)
3. [Dependencies](#dependencies)
4. [Project Structure](#project-structure)
5. [Models](#models)
6. [URLs and Routing](#urls-and-routing)
7. [API Endpoints](#api-endpoints)
8. [Django Channels](#django-channels)
9. [AWS Integration](#aws-integration)
10. [Authentication](#authentication)
11. [Business Policy Implementation](#business-policy-implementation)

## Features
- User authentication (manual and Google)
- Campaign creation and management
- Ad generation using AI models
- Real-time canvas editing with Django Channels
- Integration with AWS services (SageMaker, Lambda, S3)
- RESTful APIs with Django Rest Framework
- Business policy implementation (freemium model)

## Django Apps
The project is divided into several Django apps:
1. **accounts**: Handles user authentication and profile management.
2. **campaign**: Manages campaigns, including ad creation and storage.
3. **ads**: Manages ad components such as backgrounds, product images, and text.
4. **aws_integration**: Custom library for interacting with AWS services.

## Dependencies
Install the required dependencies using `pip`:
```sh
pip install django djangorestframework django-allauth django-rest-auth django-channels boto3 django-cors-headers
```

## Project Structure
```
adventure_backend/
    ├── accounts/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    ├── campaign/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    ├── ads/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    ├── aws_integration/
    │   ├── client.py
    │   ├── services.py
    ├── adventure_backend/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   ├── wsgi.py
    ├── manage.py
    ├── requirements.txt
```

## Models
### accounts/models.py
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

```

### campaign/models.py

```python
from django.db import models
from accounts.models import CustomUser

class Campaign(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EditRecord(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='edit_records', on_delete=models.CASCADE)
    layer_data = models.JSONField()  # Stores the editing data in JSON format, suitable for React Konva
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

```

## URLs and Routing
### adventure_backend/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/campaign/', include('campaign.urls')),
    path('api/ads/', include('ads.urls')),
]

```

### accounts/urls.py
```python
from django.urls import path
from .views import CustomUserCreate, LoginView, LogoutView

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

```

## API Endpoints
### accounts/views.py

```python
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args):
        request.user.auth_token.delete()
        return Response(status=204)

```

### campaign/views.py
```python
from rest_framework import generics, permissions
from .models import Campaign, EditRecord
from .serializers import CampaignSerializer, EditRecordSerializer

class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EditRecordListCreateView(generics.ListCreateAPIView):
    queryset = EditRecord.objects.all()
    serializer_class = EditRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        campaign = Campaign.objects.get(pk=self.request.data['campaign_id'])
        serializer.save(campaign=campaign)

```

## Django Channels
### adventure_backend/asgi.py
```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from campaign.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adventure_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

```

### campaign/routing.py
```python
from django.urls import re_path
from .consumers import EditConsumer

websocket_urlpatterns = [
    re_path(r'ws/campaign/(?P<campaign_id>\w+)/$', EditConsumer.as_asgi()),
]

```

### campaign/consumers.py

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EditConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.campaign_id = self.scope['url_route']['kwargs']['campaign_id']
        self.campaign_group_name = f'campaign_{self.campaign_id}'

        await self.channel_layer.group_add(
            self.campaign_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.campaign_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.campaign_group_name,
            {
                'type': 'edit_campaign',
                'data': data
            }
        )

    async def edit_campaign(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

```

## AWS Integration

### aws_integration/client.py

```python
import boto3

class AWSClient:
    def __init__(self):
        self.sagemaker = boto3.client('sagemaker')
        self.lambda_client = boto3.client('lambda')
        self.s3 = boto3.client('s3')

```

### aws_integration/services.py


```python
from .client import AWSClient

class SageMakerService(AWSClient):
    def invoke_endpoint(self, endpoint_name, payload):
        response = self.sagemaker.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=payload
        )
        return response['Body'].read().decode('utf-8')

class LambdaService(AWSClient):
    def invoke_function(self, function_name, payload):
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=payload
        )
        return response['Payload'].read().decode('utf-8')

```

## Authentication
Google Authentication and Manual Authentication
- Manual Authentication: Implemented using Django Rest Framework's token authentication.
- Google Authentication: Implemented using django-allauth and django-rest-auth.

### accounts/serializers.py
```python
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

```


## Business Policy Implementation
### Freemium Model:
- Guest Users: Required to watch ads before seeing results and saving high-quality images.
- Registered Users: Subscription plans for ad-free experience and access to additional features.