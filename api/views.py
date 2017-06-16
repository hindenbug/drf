# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

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
    data = request.data
    invite_code = request.GET.get('code', None)

    if invite_code is not None:
        data['code'] = invite_code

    serializer = UserSerializer(data=data, context={'request': request})

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
            return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        user.verified = True
        user.save()
        return Response({'message': 'Your account has been verified successfully.'}, status=status.HTTP_200_OK)
    except(User.DoesNotExist, ObjectDoesNotExist,):
        return Response({'error': 'Something went wrong, please try again.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def password(request):
    data = request.data
    token = request.GET.get("token")

    user = User.objects.filter(email=data["email"], password_reset_token=token).first()

    if user:
        user.set_new_password(data["password"])
        return Response({"message": "Your password was updated successfully!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((CustomTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def reset_password(request):
    user = request.user

    token = user.set_password_reset_token()

    return Response({'reset_password_link': "Here is you password reset link %s?token=%s" % \
                     (reverse("password", request=request), token)}, \
                    status=status.HTTP_200_OK)


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

@api_view(["GET"])
@authentication_classes((CustomTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def invite(request):
    user = request.user

    if user and not user.team:
        return Response({'error': 'You need to be a member of a team in order to invite other people.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'invite_link': "%s would like to invite you to join %s?code=%s" % \
                     (user.first_name + user.last_name, reverse("register", request=request), user.invite_code)}, \
                    status=status.HTTP_200_OK)
