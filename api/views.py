from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import AccessToken
@csrf_exempt
def signup_user(request):
    if request.method != 'POST': 
        return JsonResponse({'error':'only POST method used for this'},status=405)
    

    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


@csrf_exempt
def login_user(request):
    if request.method != 'POST': 
        return JsonResponse({'error':'only POST method used for this'},status=405)
    
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
def get_profile(request):
    if request.method != 'GET': 
        return JsonResponse({'error':'only GET method used for this'},status=405)
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)

    token = auth_header.split(' ')[1]

    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']  # This works with SimpleJWT

        user = User.objects.get(id=user_id)
        return JsonResponse({
            'id': user.id,
            'username': user.username
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=401)  