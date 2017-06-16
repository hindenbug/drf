# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth import authenticate

from .authentication import CustomTokenAuthentication
from .serializers import UserSerializer, TeamSerializer
from .models import User
import os, binascii

@api_view(['POST'])
def login(request):
    """
    Generate token for at login.
    """
    creds = {"email": request.data["email"], "password": request.data["password"]}
    user = authenticate(**creds)

    if not user:
        return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

    user.token = binascii.hexlify(os.urandom(20)).decode()
    user.save()

    return Response({"token": user.token})

@api_view(['POST'])
def register(request):
    """
    Register's a new user
    """
    serializer = UserSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception, error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify(request, key):
    """
    Verify user's email.
    """
    try:
        user = User.objects.get(verification_key=key)

        if user.verified:
            return Response({'error': ''}, status=status.HTTP_400_BAD_REQUEST)

        user.verified = True
        user.save()
        return Response({'message': 'Your account has been verified successfully.'}, status=status.HTTP_200_OK)
    except(User.DoesNotExist, ObjectDoesNotExist,):
        return Response({'error': 'Something went wrong, please try again.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes((CustomTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def reset_password(request):
    pass

@api_view(["POST"])
@authentication_classes((CustomTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_team(request):
    user = request.user

    if user and user.team is not None:
        return Response({'error': 'You already have a team.' }, status=status.HTTP_400_BAD_REQUEST)

    serializer = TeamSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        try:
            team = serializer.save()
            user.team = team
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError, error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
