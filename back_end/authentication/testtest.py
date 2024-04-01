import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get('email')
        api_key = 'live_37e0e3087eb02492f74c'
        
        response = requests.get(f"https://api.emailable.com/v1/verify?email={email}&api_key={api_key}")
        data = response.json()
        
        if response.status_code == 200:
            if data.get('state') == 'deliverable':
                if User.objects.filter(email=email).exists():
                    return Response({"error": "A user with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
                
                user = serializer.save()
                user.set_password(request.data['password'])
                user.is_active = False  # Setting the user's initial state to inactive
                user.save()
                
                # Send verification email
                send_verification_email(user)
                
                return Response({"message": "Verification email sent"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email address is not deliverable'}, status=status.HTTP_400_BAD_REQUEST)
        elif response.status_code == 429:
            return Response({'error': 'Rate Limit Exceeded'}, status=response.status_code)
        else:
            error_message = f"Invalid response from email validation service. Status code: {response.status_code}, Response: {response.text}"
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator

@api_view(['GET'])
def send_verification_email(request, uidb64, token):
    try:
        uid = int(uidb64)
    except ValueError:
        return JsonResponse({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, pk=uid)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({'message': 'Email successfully verified'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)
