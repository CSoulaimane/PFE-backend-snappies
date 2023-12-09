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
        commandes_data = [{'id': commande.id, 'value': commande.value} for commande in commandes]
        return HttpResponse(json.dumps(commandes_data), content_type='application/json')
    else:
        return JsonResponse({'error': 'You are not authorized to create a commande'})        


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_commande(request, commande_id):
    user = request.user
    if user.is_admin:
        try:
            commande = Commande.objects.get(id=commande_id)
            data = json.loads(request.body)
            
            # Update the fields if present in the request data
            if 'value' in data:
                commande.value = data['value']
            
            # Save the updated Commande instance
            commande.save()

            # Return the updated data as a response
            updated_data = {'id': commande.id, 'value': commande.value}
            return Response(updated_data)
        except Commande.DoesNotExist:
            return JsonResponse({'error': 'Commande not found'}, status=404)
    else:
        return JsonResponse({'error': 'You are not authorized to update a commande'})

    
    


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_commande(request):
    user = request.user
    if user.is_admin:
        data = json.loads(request.body)
        id = data.get('id')
        value = data.get('value')
        commande = Commande(id=id, value=value)
        commandes_data = {'id': commande.id, 'value': commande.value}

        commande.save()
        return Response(commandes_data)
    else:
        return JsonResponse({'error': 'You are not authorized to create a commande', 'token =': TokenAuthentication})        
    
    
def display_hello_world(request):
    message = { 'message': 'Hello World!' }
    return HttpResponse(json.dumps(message))
