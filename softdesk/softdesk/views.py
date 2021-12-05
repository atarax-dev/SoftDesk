from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from softapp.serializers import ProjectSerializer
from softapp.models import Project

from rest_framework import generics

from user.models import User
from user.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated]
        data = {
            'username': 'admin',
            'years_active': 10
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        permission_classes = [IsAuthenticated]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
