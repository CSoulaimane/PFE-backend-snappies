import json
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import Tournee, User, Etapes_tournee
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
 

    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_tournees(request):
    try:
        user = request.user
        if user.is_admin:
            tournees = Tournee.objects.all()
            tournees_data = [{'id': tourne.id_tournee, 'livreur': tourne.livreur.username ,'date': tourne.date.strftime('%Y-%m-%d')} for tourne in tournees]
            return HttpResponse(json.dumps(tournees_data), content_type='application/json')
        else:
            return JsonResponse({'error': 'You are not authorized to create a commande'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_etapes_tournees(request, id_tournee):
    try:
        user = request.user
        if user.is_admin:
            etapes_tournees = Etapes_tournee.objects.filter(tournee= id_tournee)
            etapes_tournees_data = [{'id': etapes_tournee.id_etape_tournee, 'tournee': etapes_tournee.tournee.id_tournee , 'commande' : etapes_tournee.commande.id} for etapes_tournee in etapes_tournees]
            return HttpResponse(json.dumps(etapes_tournees_data), content_type='application/json')
        else:
            return JsonResponse({'error': 'You are not authorized to create a commande'})     
    except Exception as e:
        return JsonResponse({'error': str(e)})        
    
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def assigner_tournee(request, id_tournee):
    try:
        user = request.user
        if user.is_admin:
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee)
            livreur_id = request.data.get('livreur_id')  # Assurez-vous que 'livreur_id' est fourni dans le corps de la requête
            livreur = get_object_or_404(User, id_user=livreur_id, is_admin=False)

            # Assigner la tournée au livreur
            tournee.livreur = livreur
            tournee.save()

            return JsonResponse({'success': f'Tournée assignée à {livreur.username}'})
        else:
            return JsonResponse({'error': 'You are not authorized to assign a tournee'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_tournees_livreur(request, livreur_id):
    try:
        user = request.user
        if not user.is_admin:
            livreur = get_object_or_404(User, id_user=livreur_id, is_admin=False)

            tournees = Tournee.objects.filter(livreur=livreur)
            tournees_data = [{
                'id': tournee.id_tournee,
                'livreur': tournee.livreur.username,
                'date': tournee.date.strftime('%Y-%m-%d'),
                # Ajoutez d'autres champs de la tournée selon vos besoins
            } for tournee in tournees]

            return HttpResponse(json.dumps(tournees_data), content_type='application/json')
        else:
            return JsonResponse({'error': 'Only non-admin users (livreurs) can access this endpoint'})
    except Exception as e:
        return JsonResponse({'error': str(e)})    
    
    
    
    