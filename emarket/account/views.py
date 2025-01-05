from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .models import Profile
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data
    serializer = SignUpSerializer(data=data)
    if serializer.is_valid():
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            try:
                # Create user and set the username to the email
                user = User(
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    email=email,
                    username=email  # Set username as email
                )
                user.set_password(data.get('password'))  # Handle password hashing
                user.save()

                return Response({'details': 'Your account has been registered successfully!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'This email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    # Get the authenticated user
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != "":
        user.password = make_password(data['password'])
    user.save()
    # Pass the user instance and request data to the serializer
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


def get_current_host(request):
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{protocol}://{host}/"




@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])

    # Ensure user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    token = get_random_string(40)
    expire_date = timezone.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = f"{host}api/reset_password/{token}/".format(token=token)
    body = f"Your password reset link is {link}"

    send_mail(
        "Password reset from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']],
        fail_silently=False,
    )

    return Response({"details": f"Password reset sent to {data['email']}"})




@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    # Validate input
    if not password or not confirm_password:
        return Response({"error": "Password and confirmPassword are required"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Get the profile based on the token
    profile = get_object_or_404(Profile, reset_password_token=token)

    if profile.reset_password_expire < timezone.now():
        return Response({"error": "Token is expired"}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    # Update user password
    user = profile.user
    user.set_password(password)
    user.save()

    # Clear the token and expiration date
    profile.reset_password_token = ''
    profile.reset_password_expire = None
    profile.save()

    return Response({"details": "Password has been successfully reset"}, status=status.HTTP_200_OK)




# views.py

# from django.contrib.auth.hashers import make_password
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from rest_framework import status
# from .serializers import SignUpSerializer, UserSerializer
# from rest_framework.permissions import IsAuthenticated
#
#
# @api_view(['POST'])
# def register(request):
#     data = request.data
#     serializer = SignUpSerializer(data=data)
#     if serializer.is_valid():
#         email = data.get('email')
#         if not User.objects.filter(email=email).exists():
#             try:
#                 serializer.save()
#                 return Response({'details': 'Your account has been registered successfully!'},
#                                 status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response({'error': 'This email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def current_user(request):
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data)
#
#
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_user(request):
#     user = request.user
#     data = request.data
#
#     user.first_name = data.get('first_name', user.first_name)
#     user.last_name = data.get('last_name', user.last_name)
#     user.email = data.get('email', user.email)
#
#     if 'password' in data and data['password']:
#         user.password = make_password(data['password'])
#
#     user.save()
#     serializer = UserSerializer(user)
#     return Response(serializer.data)


