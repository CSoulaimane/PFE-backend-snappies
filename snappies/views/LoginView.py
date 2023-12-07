import json
from django.contrib.auth import authenticate, login as auth_login  
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from django.utils import timezone

from ..models import User

# users/views.py

def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin')

        user = User( username=username, password=password, is_admin=is_admin)
        user.set_password(password) # hash the password
        user_data = {'id_user': user.id_user, 'username': user.username , 'password': user.password , 'is_admin': user.is_admin}

        user.save()
        
        authenticate_user = authenticate(request, username=username , password=password)
        print(authenticate_user)
        return HttpResponse(json.dumps(user_data))
    else:
        return HttpResponse('error')



def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id_user=user_id)
            user.delete()
            return JsonResponse({'message': f'User {user_id} deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with id {user_id} does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
def getAll(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = [{'id_user': user.id_user, 'username': user.username} for user in users]
        return HttpResponse(json.dumps(users_data), content_type='application/json')    
    
def is_admin(user):
    return user.is_admin
    
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        User = get_user_model()
        print(User)
        authenticate_user = authenticate(request, username=username , password=password)
        print(authenticate_user)
        
       
        if authenticate_user is not None:
            # Authentification réussie, maintenant pn appel le login
            auth_login(request, authenticate_user)
            
            token, created = Token.objects.get_or_create(user=authenticate_user)

            if authenticate_user.is_admin:
                role='admin'
            else:
                role='livreur'
            
            return JsonResponse({'message': 'Login is valid', 'role':role , 'token':token.key})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
def logout_user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found', 'user not found ':user}, status=404)

    logout(request)

    return JsonResponse({'message': f'Logout successful for user: {username}'})

