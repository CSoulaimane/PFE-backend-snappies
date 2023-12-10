

import json
from django.http import HttpResponse, JsonResponse

from ..models import Commande
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def get_commande(request, commande_id):
    if request.method == 'GET':
        try:
            commande = Commande.objects.get(id=commande_id)
            commande_data = {'id': commande.id, 'value': commande.value}
            return HttpResponse(json.dumps(commande_data), content_type='application/json')
        except Commande.DoesNotExist:
            return HttpResponse(status=404)
        
        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_commandes(request):
    user = request.user
    if user.is_admin:
        commandes = Commande.objects.all()
        commandes_data = [{'id_commande': commande.id_commande, 'client': commande.client.name, 'default': commande.default, 'est_modifie': commande.est_modifie, 'tournee': commande.tournee.nom} for commande in commandes]
        return JsonResponse({'commandes': commandes_data})
    else:
        return JsonResponse({'error': 'You are not authorized to get commandes'})
      

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_commande(request, commande_id):
    user = request.user
    if user.is_admin:
        try:
            commande = Commande.objects.get(id_commande=commande_id)
            data = json.loads(request.body)

            if 'client' in data:
                commande.client_id = data['client']
            if 'default' in data:
                commande.default = data['default']
            if 'est_modifie' in data:
                commande.est_modifie = data['est_modifie']
            if 'tournee' in data:
                commande.tournee_id = data['tournee']

            commande.save()

            updated_data = {'id_commande': commande.id_commande, 'client': commande.client.name, 'default': commande.default, 'est_modifie': commande.est_modifie, 'tournee': commande.tournee.nom}
            return JsonResponse({'commande': updated_data})
        except Commande.DoesNotExist:
            return JsonResponse({'error': 'Commande not found'}, status=404)
    else:
        return JsonResponse({'error': 'You are not authorized to update a commande'})


    
    

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def commande_livre(request, commande_id):
    try:
        commande = Commande.objects.get(id_commande=commande_id)
    except Commande.DoesNotExist:
        return JsonResponse({'error': f'Commande with id {commande_id} does not exist'}, status=404)

    commande.est_livre = True
    commande.save()

    return JsonResponse({'message': f'Commande {commande_id} marquée comme livrée'})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_commande(request):
    user = request.user
    if user.is_admin:
        data = json.loads(request.body)
        id_commande = data.get('id_commande')
        client_id = data.get('client')
        default = data.get('default')
        est_modifie = data.get('est_modifie')
        tournee_id = data.get('tournee')

        commande = Commande(id_commande=id_commande, client_id=client_id, default=default, est_modifie=est_modifie, tournee_id=tournee_id)

        commande.save()

        created_data = {'id_commande': commande.id_commande, 'client': commande.client.name, 'default': commande.default, 'est_modifie': commande.est_modifie, 'tournee': commande.tournee.nom}
        return JsonResponse({'commande': created_data})
    else:
        return JsonResponse({'error': 'You are not authorized to create a commande'})
    
    
    
def display_hello_world(request):
    message = { 'message': 'Hello World!' }
    return HttpResponse(json.dumps(message))
