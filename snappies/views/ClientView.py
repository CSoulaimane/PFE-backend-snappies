import json
from django.http import HttpResponse, JsonResponse

from ..models import Client,Commande,Caisse_commande
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import connection




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_clients_free(request):

    user = request.user
    if user.is_admin:
        try :
    
            clients_list = []
            with connection.cursor() as cursor:
                cursor.execute("select cl.* from snappies_client cl where cl.id_client not in (select c.client_id from snappies_commande c)")
                results = cursor.fetchall()
                for row in results:
                    client = {
                        'id': row[0],
                        'client_nom': row[1],
                        'telephone': row[2],
                        'adresse': row[3],
                        # Ajoutez d'autres champs si nécessaire
                    }
                    clients_list.append(client)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(clients_list,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_409_CONFLICT)
    



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_client(request):
        data = json.loads(request.body)
        name = data.get('name')
        numero_telephone = data.get('numero_telephone')
        adresse = data.get('adresse')
        client = Client(name=name, numero_telephone=numero_telephone , adresse=adresse)
        client_data = {'name': client.name, 'numero_telephone': client.numero_telephone , 'adresse': client.adresse}

        client.save()
        return HttpResponse(json.dumps(client_data))

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_client(request, id_client):
    try:
        client = Client.objects.get(id_client=id_client)
    except Client.DoesNotExist:
        return JsonResponse({'error': f'Client with id {id_client} does not exist'}, status=404)

    client_data = {
        'id': client.id_client,
        'name': client.name,
        'numero_telephone': client.numero_telephone,
        'adresse': client.adresse,
        # Add other fields if necessary
    }

    return JsonResponse(client_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_client(request, id_client):
        try:
            client = Client.objects.get(id_client=id_client)
            
            commandes_client = Commande.objects.filter(client=client)
            for c in commandes_client:
                for cc in Caisse_commande.objects.filter(commande=c):
                    cc.delete()
                c.delete()    

            client.delete()
            
            return JsonResponse({'message': f'Client {id_client} deleted successfully'})
        except Client.DoesNotExist:
            return JsonResponse({'error': f'Client with id {id_client} does not exist'}, status=404)
    
    
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_client(request, id_client):
    try:
        client = Client.objects.get(id_client=id_client)
    except Client.DoesNotExist:
        return JsonResponse({'error': f'Client with id {id_client} does not exist'}, status=404)

    data = json.loads(request.body)
    
    if 'name' in data:
        client.name = data['name']
    if 'numero_telephone' in data:
        client.numero_telephone = data['numero_telephone']
    if 'adresse' in data:
        client.adresse = data['adresse']

    client.save()

    client_data = {
        'name': client.name,
        'numero_telephone': client.numero_telephone,
        'adresse': client.adresse
    }

    return HttpResponse(json.dumps(client_data))