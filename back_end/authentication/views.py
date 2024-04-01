from django.shortcuts import get_object_or_404
from .models import User,Candidate,CustomToken
from .serializers import UserSerializer,CandidateSerializer
from rest_framework.decorators import api_view ,authentication_classes,permission_classes
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import timedelta


@api_view(['POST'])
def login(request):
    user=get_object_or_404(User,email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"not found "},status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer=UserSerializer(instance=user)
    return Response({"token": token.key, "status":status.HTTP_200_OK,"user":serializer.data})
1

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        email=request.data.get('email')

        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        user.set_password(request.data['password'])
        user.is_active = False  # Setting the user's initial state to inactive
        user.save()

        # Generate and save token with expiration time
        token = default_token_generator.make_token(user)
        expiration_time = timezone.now() + timedelta(minutes=15)
        CustomToken.objects.create(user=user, token=token, expiration_date=expiration_time)
        
        # Generate verification URL
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f"http://127.0.0.1:8000/authentication/email_verified/{uidb64}/{token}/"

        # Send verification email
        subject = 'Verify your email address'
        message = f'Click the following link to verify your email address: {verification_url}'
        recipient_email = user.email
        send_mail(subject, message, None, [recipient_email])
        return Response({"message": "Verification email sent"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def email_verified(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        custom_token = CustomToken.objects.get(user=user, token=token)
    except CustomToken.DoesNotExist:
        return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)
        
    if timezone.now() > custom_token.expiration_date:
        return Response({'error': 'Verification link has expired'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user.is_active = True
        user.save()
        custom_token.delete()
        
        return Response({'message': 'Email successfully verified'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate and save token with expiration time
    token = default_token_generator.make_token(user)
    expiration_time = timezone.now() + timedelta(minutes=15)
    CustomToken.objects.create(user=user, token=token, expiration_date=expiration_time)
    
    # Generate password reset URL
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"http://127.0.0.1:8000/authentication/reseted_password/{uidb64}/{token}/"

    # Send verification email
    subject = 'Reset Your Password'
    message = f'Click the following link to reset your password: {verification_url}'
    recipient_email = user.email
    send_mail(subject, message, None, [recipient_email])
    
    return Response({"message": "Check your email for password reset instructions"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reseted_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        custom_token = CustomToken.objects.get(user=user, token=token)
    except CustomToken.DoesNotExist:
        return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)
        
    if timezone.now() > custom_token.expiration_date:
        return Response({'error': 'Verification link has expired'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Assuming you have a form where the user provides a new password
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error': 'New password not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        custom_token.delete()
        
        return Response({'message': 'Password successfully reset'}, status=status.HTTP_200_OK)