from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView

class Register(CreateAPIView):
    serializer_class = UserSerializer