

import json
from django.forms import model_to_dict
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
def commande_livre(request, commande_id):
    try:
        commande = Commande.objects.get(id_commande=commande_id)
    except Commande.DoesNotExist:
        return JsonResponse({'error': f'Commande with id {commande_id} does not exist'}, status=404)

    commande.est_livre = True
    commande.save()

    return JsonResponse({'message': f'Commande {commande_id} marquée comme livrée'})




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_commandes(request):

    user = request.user
    if user.is_admin:
        

        



        return JsonResponse({'commandes': commandes_data})
    else:
        return JsonResponse({'error': 'You are not authorized to get commandes'})


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_commande_admin(request, id_commande):
    user = request.user
    if user.is_admin:
        try:
            data = json.loads(request.body)
             
            id_client = data["id_client"]
            articles = data["articles"]

            commande = Commande.objects.get(id_commande=id_commande)
            tab_articles = [];
            created_data = {"id_commande" :id_commande, "id_client" :id_client,"articles":tab_articles}
            for a in articles:
                article = Article.objects.get(id_article=a["id_article"])
                caisse = Caisse.objects.get(article=article)
                print(article,caisse)
                caisse_commande = Caisse_commande.objects.get(commande=commande,caisse=caisse)
                if  a["is_deleted"] == "true":
                        caisse_commande.delete()
                elif a["unite"] != 0:
                    caisse_commande.unite = a["unite"]
                    caisse_commande.save()
                    tab_articles.append({"id_article":a["id_article"],
                                        "nbr_caisses":caisse_commande.nbr_caisses,
                                        "unite":caisse_commande.unite })
                else:
                    caisse_commande.nbr_caisses = a["nbr_caisses"]
                    caisse_commande.save()
                    tab_articles.append({"id_article":a["id_article"],
                                        "nbr_caisses":caisse_commande.nbr_caisses,
                                        "unite":caisse_commande.unite })


            return JsonResponse({'commande': created_data})
        except Exception as e:
            print(f"Erreur : {e}")
    else:
        return JsonResponse({'error': 'You are not authorized to update a commande'})
   
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_commande(request):
    user = request.user
    try:
        if user.is_admin:           
            data = json.loads(request.body)
             
            id_client = data["id_client"]
            articles = data["articles"]
            id_tournee = data["id_tournee"]

            clientDejaTournee = Commande.objects.filter(client=id_client)
            tourneeExistePas = not Tournee.objects.filter(id_tournee=id_tournee)
            if clientDejaTournee.exists():
                return Response(status=status.HTTP_409_CONFLICT)
            if tourneeExistePas:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            
            print("eddd")
            commandeDefaut = Commande(tournee_id=id_tournee, client_id=id_client, default=True, est_modifie=False, est_livre=False)
            print("mlm")
            commandeModifie = Commande(tournee_id=id_tournee, client_id=id_client, default=False, est_modifie=False, est_livre=False)
            print("defaut ", commandeDefaut)
            print("modifie ", commandeModifie)
            commandeDefaut.save()
            commandeModifie.save()
        
            print("apres defaut " , commandeDefaut)
            print("apres modifie ", commandeModifie)

            tab_articles = []
            data_created = {"commandeDefaut":{"id_commande" : commandeDefaut.id_commande,"id_client":id_client, "articles":tab_articles },
                            "commandeModifie":{"id_commande" : commandeModifie.id_commande,"id_client":id_client ,"articles": tab_articles } }
            for a in articles:
                if a["nbr_caisses"] != 0 and a["unite"] != 0:
                    commandeDefaut.delete()
                    commandeModifie.delete()
                    return Response(status= status.HTTP_400_BAD_REQUEST)
                id_article=a["id_article"]
                articlesNonExsistant = not Article.objects.filter(id_article=id_article)
                if articlesNonExsistant:
                    commandeDefaut.delete()
                    commandeModifie.delete()
                    return Response(status= status.HTTP_404_NOT_FOUND)
                caisse = Caisse.objects.get(article=id_article)
                article = Article.objects.get(id_article=id_article)

                if a["nbr_caisses"] != 0 :
                    caisse_commande_defaut = Caisse_commande(caisse=caisse,commande=commandeDefaut,nbr_caisses=a["nbr_caisses"],unite=0)
                    caisse_commande_modifie = Caisse_commande(caisse=caisse,commande=commandeModifie,nbr_caisses=a["nbr_caisses"],unite=0)
                    caisse_commande_modifie.save()
                    caisse_commande_defaut.save()
                    tab_articles.append({"id_article":id_article,"type" : article.types,"taille": article.taille ,
                                        "nbr_articles":caisse.nbr_articles,"nbr_caisses":caisse_commande_defaut.nbr_caisses,"unite":caisse_commande_defaut.unite })

                elif a["unite"] != 0 :
                    caisse_commande_defaut = Caisse_commande(caisse=caisse,commande=commandeDefaut,nbr_caisses=0,unite= a["unite"])
                    caisse_commande_modifie = Caisse_commande(caisse=caisse,commande=commandeModifie,nbr_caisses=0,unite= a["unite"])
                    caisse_commande_modifie.save()
                    caisse_commande_defaut.save()
                    tab_articles.append({"id_article":id_article,"type" : article.types,"taille": article.taille ,
                                        "nbr_articles":caisse.nbr_articles,"nbr_caisses":caisse_commande_defaut.nbr_caisses,"unite":caisse_commande_defaut.unite })




            return Response(data_created,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'You are not authorized to create a commande'})
        
    except Exception as e:
        print(f"Erreur : {e}")



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_commandes(request):
    try:
        user = request.user
        if user.is_admin:
            commands = Commande.objects.filter(default=True)

            commands_data = []
            for command in commands:
                command_data = model_to_dict(command)
                caisse_commandes = Caisse_commande.objects.filter(commande=command.id_commande)
                articles_data = []

                for caisse_commande in caisse_commandes:
                    article_data = model_to_dict(caisse_commande.caisse.article)
                    article_data['nbr_caisses'] = caisse_commande.nbr_caisses
                    article_data['unite'] = caisse_commande.unite
                    articles_data.append(article_data)

                command_data['caisse_commandes'] = list(caisse_commandes.values())
                command_data['articles'] = articles_data

                commands_data.append(command_data)

            return Response({'commands': commands_data})
        else:
            return Response({'error': 'You are not authorized to view admin commands'})
    except Exception as e:
        return Response({'error': str(e)})
    
    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_livreur_commandes(request):
    try:
        user = request.user
        if not user.is_admin:
            base_commands = Commande.objects.filter( default=True, est_modifie=False)
            modified_commands = Commande.objects.filter( default=False, est_modifie=True)

            commands_data = []
            
            # Ajouter les commandes de base
            for base_command in base_commands:
                command_data = model_to_dict(base_command)
                caisse_commandes = Caisse_commande.objects.filter(commande=base_command.id_commande)
                articles_data = []

                for caisse_commande in caisse_commandes:
                    article_data = model_to_dict(caisse_commande.caisse.article)
                    article_data['nbr_caisses'] = caisse_commande.nbr_caisses
                    article_data['unite'] = caisse_commande.unite
                    articles_data.append(article_data)

                command_data['caisse_commandes'] = list(caisse_commandes.values())
                command_data['articles'] = articles_data

                commands_data.append(command_data)

            # Ajouter les commandes modifiées si elles existent
            if modified_commands.exists():
                modified_command = modified_commands.first()
                command_data = model_to_dict(modified_command)
                caisse_commandes = Caisse_commande.objects.filter(commande=modified_command.id_commande)
                articles_data = []

                for caisse_commande in caisse_commandes:
                    article_data = model_to_dict(caisse_commande.caisse.article)
                    article_data['nbr_caisses'] = caisse_commande.nbr_caisses
                    article_data['unite'] = caisse_commande.unite
                    articles_data.append(article_data)

                command_data['caisse_commandes'] = list(caisse_commandes.values())
                command_data['articles'] = articles_data

                commands_data.append(command_data)

            return Response({'commands': commands_data})
        else:
            return Response({'error': 'You are not authorized to view livreur commands'})
    except Exception as e:
        return Response({'error': str(e)})