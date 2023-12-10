

import json
from django.http import HttpResponse, JsonResponse

from ..models import Commande,Tournee,Caisse_commande,Caisse,Article
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
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


    
    


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_commande(request):
    user = request.user
    if user.is_admin:
        data = json.loads(request.body)
        id_client = data["id_client"]
        articles = data["articles"]
        id_tournee = data["id_tournee"]
        
       
        clientDejaTournee = Commande.objects.filter(client=id_client)
        tourneeExistePas = not Tournee.objects.filter(id_tournee=id_tournee)
        if clientDejaTournee.exists():
            return Response(status=status.HTTP_409_CONFLICT)
        if tourneeExistePas.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        commandeDefaut = Commande(tournee=id_tournee,client =id_client,default=True,est_modifie=False,est_livre =False)
        commandeModifie = Commande(tournee=id_tournee,client =id_client,default=False,est_modifie=False,est_livre =False)
        print(commandeDefaut)
        commandeDefaut.save()
        print(commandeDefaut)
        commandeModifie.save()

        for a in articles:
            if a["nbr_caisses"] != 0 & a["unite"] != 0:
                return Response(status= status.HTTP_400_BAD_REQUEST)
            id_article=a["id_article"]
            articlesNonExsistant = not Article.objects.filter(id_article=id_article)
            if articlesNonExsistant:
                return Response(status= status.HTTP_404_NOT_FOUND)
            caisse = Caisse.objects.get(article=id_article)
            if a["nbr_caisses"] != 0 :
                caisse_commande_defaut = Caisse_commande(caisse=caisse,commande=commandeDefaut.id_commande,nbr_caisses=a["nbr_caisses"],unite=0)
                caisse_commande_ = Caisse_commande(caisse=caisse,commande=commandeDefaut.id_commande,nbr_caisses=a["nbr_caisses"],unite=0)

                caisse_commande_initial.save()
            elif a["unite"] != 0 :
                caisse_commande_initial = Caisse_commande(caisse=caisse,commande=commandeDefaut.id_commande,nbr_caisse=0,unite= a["unite"])
                caisse_commande_initial.save()

        return JsonResponse({'commande': "re"})
    else:
        return JsonResponse({'error': 'You are not authorized to create a commande'})
    
    
    
def display_hello_world(request):
    message = { 'message': 'Hello World!' }
    return HttpResponse(json.dumps(message))
