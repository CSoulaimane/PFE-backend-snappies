import json
from django.http import HttpResponse, JsonResponse

from ..models import Client
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



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


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_client(request, id_client):
        try:
            client = Client.objects.get(id_client=id_client)
            client.delete()
            return JsonResponse({'message': f'Client {id_client} deleted successfully'})
        except Client.DoesNotExist:
            return JsonResponse({'error': f'Client with id {id_client} does not exist'}, status=404)
    
    
    
def display_hello_world(request):
    message = { 'message': 'Hello World!' }
    return HttpResponse(json.dumps(message))
