

import json
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from ..models import Commande,Tournee,Caisse_commande,Caisse,Article,Client
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required

from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import connection

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
def get_commandes_tournee_admin(request,id_tournee):

    try:
        user = request.user
        # Vérifiez si l'utilisateur est un livreur (non-administrateur)
        if  user.is_admin:
    
            # Si l'utilisateur est un administrateur, permettez l'accès à toutes les tournées
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee)

            # Récupérez toutes les commandes de la tournée avec les détails des articles
            commandes_tournee = Commande.objects.filter(tournee=tournee,default=True)
            commandes_data = []

            for commande in commandes_tournee:
                # Si la commande est modifiée, affichez la version modifiée, sinon la version de base
                
                articles_commande = [{
                    'id_article': caisse_commande.caisse.article.id_article,
                    'nom_article': caisse_commande.caisse.article.nom,
                    'nombre_articles': caisse_commande.caisse.nbr_articles,
                    'taille_article': caisse_commande.caisse.article.taille,
                    'quantite_caisse': float(caisse_commande.nbr_caisses),
                    'quantite_unite': int(caisse_commande.unite),
                } for caisse_commande in Caisse_commande.objects.filter(commande=commande)]

                commande_data = {
                    'id_commande': commande.id_commande,
                    'client': commande.client.name,
                    'client_adresse':commande.client.adresse,
                    'default': commande.default,
                    'est_modifie': commande.est_modifie,
                    'articles': articles_commande,
                    # Ajoutez d'autres champs de la commande selon vos besoins
                }

                commandes_data.append(commande_data)

        return HttpResponse(json.dumps(commandes_data), content_type='application/json')
    except Exception as e:
        return JsonResponse({'error': str(e)})
      

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_livraison(request,id_commande):
    print("ee")
    try:
        # Vérifiez si l'utilisateur est un livreur (non-administrateur)
        commande = Commande.objects.get(id_commande=id_commande)
        print(commande.default)
        if commande.default == True:
            commande.est_livre=True
            commande.est_modifie=False
            commande_modif = Commande.objects.get(client=commande.client,default=False)
            commande_modif.est_modifie=False
            commande_modif.save()
            commande.save()
        else:
            commande.est_modifie=False
            commande_default=Commande.objects.get(client=commande.client,default=True)
            commande_default.est_livre=True
            commande_default.est_modifie=False
            commande_default.save()

        return Response({"modifie" : "true"},status=status.HTTP_200_OK)
    
    except Exception as e:
        print("ici" , e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_est_livre(request):

    try:
        # Vérifiez si l'utilisateur est un livreur (non-administrateur)
        commandes = Commande.objects.all()
        
        for c in commandes:
            c.est_livre= False
            c.save()

        return Response({"est_livre" : "maitenant à false"},status=status.HTTP_200_OK)
    
    except Exception as e:
        print("ici" , e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_commandes_tournee_modifie_ou_non(request,id_tournee):

    print("test")
    with connection.cursor() as cursor:
        print("test")
        cursor.execute(
            """
            SELECT 
                c.id_commande                      
            FROM 
                snappies_commande c
                
            WHERE  
                (
                    (c."default" = true AND c.est_modifie = false) 
                    OR 
                    (c."default" = false AND c.est_modifie = true)
                )
                
                AND c.tournee_id=%s
        """       
        ,[id_tournee]
        )
        
        rows = cursor.fetchall()
        id_list = [row[0] for row in rows]
        print(id_list )

    commandes_tournee =[]
    commandes_data = []

    for id in id_list:
        commande =Commande.objects.get(id_commande=id)
        commandes_tournee.append(commande)

    for commande in commandes_tournee:
        # Si la commande est modifiée, affichez la version modifiée, sinon la version de base

        articles_commande = [{
            'id_article': caisse_commande.caisse.article.id_article,
            'nom_article': caisse_commande.caisse.article.nom,
            'nombre_articles': caisse_commande.caisse.nbr_articles,
            'taille_article': caisse_commande.caisse.article.taille,
            'quantite_caisse': float(caisse_commande.nbr_caisses),
            'quantite_unite': int(caisse_commande.unite),
        } for caisse_commande in Caisse_commande.objects.filter(commande=commande)]
       
        commande_data = {
            'id_commande': commande.id_commande,
            'client': commande.client.name,
            "est_livre" : commande.est_livre,
            'client_adresse': commande.client.adresse,
            'default': commande.default,
            'est_modifie': commande.est_modifie,
            'articles': articles_commande,

            # Ajoutez d'autres champs de la commande selon vos besoins
        }

        
        if(commande.default == True):
            client = Client.objects.get(id_client=commande.client.id_client)
            commande_modifie = Commande.objects.get(client=client,default=False)
            print("sss")
            commande_data["id_commande"]=commande_modifie.id_commande

        commandes_data.append(commande_data)


    return HttpResponse(json.dumps(commandes_data), content_type='application/json')



@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
def commande_livre(request, commande_id):
    try:
        commande = Commande.objects.get(id_commande=commande_id)
    except Commande.DoesNotExist:
        return JsonResponse({'error': f'Commande with id {commande_id} does not exist'}, status=404)

    commande.est_livre = True
    commande.save()

    return JsonResponse({'message': f'Commande {commande_id} marquée comme livrée'})




@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_commande_admin(request, id_commande):
    id_commande=int(id_commande)
    user = request.user
    if user.is_admin:
        try:
            data = json.loads(request.body)
            print("ici")
            articles = data["articles"]
            print("ici")


            commande = Commande.objects.get(id_commande=id_commande)
            client = commande.client
            id_client=client.id_client

            # syncronsier commande par defaut et modifie
            if commande.default == True:
                print("laaaaaaaaaaaa")
                commande_modifie = Commande.objects.get(client=commande.client,default=False)    
                with connection.cursor() as cursor:
                    # Créer un tuple d'arguments pour la requête SQL
                    args = (commande.tournee.id_tournee, commande_modifie.id_commande,commande.tournee.id_tournee,commande.id_commande)

                    cursor.execute(
                        """
                        select  cc.id_caisse_commande
                        from snappies_caisse_commande cc,snappies_commande c
                        where cc.commande_id = c.id_commande
                        and c."default" = false
                        and c.tournee_id = %s
                        and c.id_commande= %s
                        and cc.caisse_id not in (

                            select ccDefault.caisse_id
                            from snappies_caisse_commande ccDefault,snappies_commande c2
                            where  c2."default" =true
                            and c2.id_commande = ccDefault.commande_id
                            and c2.tournee_id=%s
                            and c2.id_commande= %s
                            )
                        """,
                        args
                    )
                    rows = cursor.fetchall()
                    list_caisse_commandes_id = [row[0] for row in rows]
                    print("iciiiii", list_caisse_commandes_id) 
                for id in list_caisse_commandes_id:
                    c = Caisse_commande.objects.get(id_caisse_commande=id)
                    c.delete()
                    print("supprimer")

            #mettre a jour les infos pour dire que la commande d un client a ete modifie temporairement
            if commande.default == False:
                commande_defaut = Commande.objects.get(client=commande.client,default=True)
                commande_defaut.est_modifie=True
                commande.est_modifie=True
                commande.save()
                commande_defaut.save()
            tab_articles = [];
            created_data = {"id_commande" :id_commande, "id_client" :id_client,"articles":tab_articles}



            for a in articles:
                print("teststddd",a)
                article = Article.objects.get(id_article=a["id_article"])
                caisse = Caisse.objects.get(article=article)
                if a["is_created"] != "true":
                    print("is_created")
                    caisse_commande = Caisse_commande.objects.get(commande=commande,caisse=caisse)
                if commande.default == True and a["is_created"] != "true" :
                    print("testst")
                    commande_modifie = Commande.objects.get(client=client,default=False)
                    caisse_commande_modifie =Caisse_commande.objects.filter(commande=commande_modifie,caisse=caisse)
                    if caisse_commande_modifie.exists and len(caisse_commande_modifie) > 0:
                        print("ici : ",caisse_commande_modifie)
                        caisse_commande_modifie = caisse_commande_modifie[0]
                        print(caisse_commande_modifie)
                    else:
                        caisse_commande_modifie= Caisse_commande(caisse=caisse,commande=commande_modifie,nbr_caisses=caisse_commande.nbr_caisses,unite=caisse_commande.unite)
                        caisse_commande_modifie.save()
                        print(caisse_commande_modifie)

                if  a["is_deleted"] == "true":
                    print("deleted")
                    caisse_commande.delete()
                    if commande.default == True:
                        caisse_commande_modifie.delete()
                elif a["is_created"] == "true":
                    print("creteeed")
                    if commande.default == True:
                        new_caisse_commande = Caisse_commande(commande=commande,caisse=caisse,nbr_caisses=a["nbr_caisses"],unite=a["unite"])
                        new_caisse_commande_modifie = Caisse_commande(commande=commande_modifie,caisse=caisse,nbr_caisses=a["nbr_caisses"],unite=a["unite"])
                        new_caisse_commande.save()
                        new_caisse_commande_modifie.save()
                    else:
                        new_caisse_commande_modifie = Caisse_commande(commande=commande,caisse=caisse,nbr_caisses=a["nbr_caisses"],unite=a["unite"])
                        new_caisse_commande_modifie.save()
                    tab_articles.append({"id_article":a["id_article"],
                                        "nbr_caisses":float(new_caisse_commande.nbr_caisses),
                                        "unite":new_caisse_commande.unite })                    
                elif a["unite"] != 0:
                    print("unite")
                    caisse_commande.unite = a["unite"]
                    caisse_commande.save()
                    if commande.default == True:
                        caisse_commande_modifie.unite = a["unite"]
                        caisse_commande_modifie.save()
                    tab_articles.append({"id_article":a["id_article"],
                                        "nbr_caisses":float(caisse_commande.nbr_caisses),
                                        "unite":caisse_commande.unite })
                else:
                    print("nbr_caisses")
                    caisse_commande.nbr_caisses = a["nbr_caisses"]
                    caisse_commande.save()
                    if commande.default == True:
                        caisse_commande_modifie.nbr_caisses = a["nbr_caisses"]
                        caisse_commande_modifie.save()
                    tab_articles.append({"id_article":a["id_article"],
                                        "nbr_caisses":float(caisse_commande.nbr_caisses),
                                        "unite":caisse_commande.unite })


            return JsonResponse({'commande': created_data})
        except Exception as e:
            print(f"Erreur : {e}")
    else:
        return Response(status=status.HTTP_409_CONFLICT)
   
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