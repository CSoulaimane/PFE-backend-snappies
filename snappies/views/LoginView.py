import json
from django.contrib.auth import authenticate, login as auth_login  
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import User,Tournee

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


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, id_user):
    print("jkj")
    try:
        print("dede")
        livreur = User.objects.get(id_user=id_user)

    
        print(livreur)
        tournees = Tournee.objects.filter(livreur=livreur)
        print("")
        for t in tournees:
            print(t)
            t.livreur=None
            t.save()
            print("dede")
        print("dds")
        try:
            livreur.delete()
        except Exception as e:
            print("ici")
            print(f"Erreur : {e}")

        return JsonResponse({'message': f'User {id_user} deleted successfully'})
    except Exception as e:
        print(e)
   
 

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_livreurs(request):
    user= request.user
    if user.is_admin:
        # Filtrer les utilisateurs qui ne sont pas des administrateurs
        livreurs = User.objects.filter(is_admin=False)
        livreurs_data = [{'id_user': livreur.id_user, 'username': livreur.username} for livreur in livreurs]
        return HttpResponse(json.dumps(livreurs_data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error': 'Invalid credentials'}), content_type="application/json", status=401)

    
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
            
            request.session['username']= authenticate_user.get_username()
            print("hey je suis connecte")
            response_data = {'message': 'Login is valid','username': username , 'role': role, 'token': token.key}
            
            if 'username' in request.session:
                print("Session créée avec succès. Nom d'utilisateur:", request.session['username'])
            else:
                print("Échec de la création de la session.")

            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
        else:
            return HttpResponse(json.dumps({'error': 'Invalid credentials'}), content_type="application/json", status=401)
    else:
            return HttpResponse(json.dumps({'error': 'Invalid request method'}), content_type="application/json", status=405)
    

def load_user_data(request):
    if request.user.is_authenticated:
        user = request.user
        user_data = {
            'username': user.username,
            'role': 'admin' if user.is_admin else 'livreur',  # Adjust this based on your User model
        }
        return JsonResponse(user_data)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    
        
def logout_user(request):
  token = request.path.split('/')[-1]

  if token:
    user = User.objects.get(token=token)
    logout(request)
    return JsonResponse({'message': f'Déconnexion réussie pour user : {user.username} '})
  else:
    return JsonResponse({'error': 'Token invalide'}, status=401)

