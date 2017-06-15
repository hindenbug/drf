# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer
from .models import User

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
