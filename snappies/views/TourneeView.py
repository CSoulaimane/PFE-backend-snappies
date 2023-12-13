
from gettext import translation
import json
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import  Caisse_commande, Commande, Tournee, User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
 

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def creer_tournee(request):
    try:
        user = request.user
        if user.is_admin:
            nom_tournee = request.data.get('nom')  # Assurez-vous que 'nom' est fourni dans le corps de la requête

                # Créer la tournée
            tournee = Tournee.objects.create(nom=nom_tournee)

            return JsonResponse({'success': f'Tournée créée avec succès', 'id_tournee': tournee.id_tournee})
        else:
            return JsonResponse({'error': 'Vous n\'êtes pas autorisé à créer une tournée'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_tournee(request, id_tournee):
    try:
        user = request.user

        if user.is_admin:
            # Retrieve the tournee object or return 404 if not found
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee)

            # Delete the tournee
            tournee.delete()

            return JsonResponse({'success': f'Tournee {id_tournee} deleted successfully'})
        else:
            return JsonResponse({'error': 'You are not authorized to delete a tournee'})

    except Exception as e:
        return JsonResponse({'error': str(e)})    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_tournees(request):
    try:
        user = request.user
        if user.is_admin:
            tournees = Tournee.objects.all()
            tournees_data = [{'id': tourne.id_tournee, 'livreur': tourne.livreur.username if tourne.livreur else None, 'nom': tourne.nom} for tourne in tournees]
            return HttpResponse(json.dumps(tournees_data), content_type='application/json')
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
def get_tournees_livreur(request, username_livreur):
    

    try:
        user = request.user

        if not user.is_admin:

            livreur = get_object_or_404(User, username=username_livreur, is_admin=False)
            tournees = Tournee.objects.filter(livreur=livreur)
            tournees_data = [{
                'id_tournee': tournee.id_tournee,
                'livreur': tournee.livreur.username,
                'nom': tournee.nom,
                
            } for tournee in tournees]

            return HttpResponse(json.dumps(tournees_data), content_type='application/json')

        else:
            return JsonResponse({'error': 'You are not authorized to retrieve tournees for a specific livreur'})

    except Exception as e:
        return JsonResponse({'error': str(e)})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_commandes_tournee(request, id_tournee):
    try:
        user = request.user

        # Vérifiez si l'utilisateur est un livreur (non-administrateur)
        if not user.is_admin:
            livreur = user

            # Vérifiez si la tournée appartient au livreur
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee, livreur=livreur)

            # Récupérez toutes les commandes de la tournée
            commandes_tournee = Commande.objects.filter(tournee=tournee)
            commandes_data = [{
                'id_commande': commande.id_commande,
                'client': commande.client.name,
                'default': commande.default,
                'est_modifie': commande.est_modifie,
                'tournee': id_tournee
                # Ajoutez d'autres champs de la commande selon vos besoins
            } for commande in commandes_tournee]

            return HttpResponse(json.dumps(commandes_data), content_type='application/json')
        else:
            # Si l'utilisateur est un administrateur, permettez l'accès à toutes les tournées
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee)

            # Récupérez toutes les commandes de la tournée
            commandes_tournee = Commande.objects.filter(tournee=tournee)
            commandes_data = [{
                'id_commande': commande.id_commande,
                'client': commande.client.name,
                'default': commande.default,
                'est_modifie': commande.est_modifie,
                'tournee': id_tournee
                # Ajoutez d'autres champs de la commande selon vos besoins
            } for commande in commandes_tournee]

            return HttpResponse(json.dumps(commandes_data), content_type='application/json')
       
    except Exception as e:
        return JsonResponse({'error': str(e)})

    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_details_commandes_tournee(request, id_tournee):
    try:
        user = request.user

        # Vérifiez si l'utilisateur est un livreur (non-administrateur)
        if not user.is_admin:
            livreur = user
#            commands = Commande.objects.filter(default=True)

            # Vérifiez si la tournée appartient au livreur
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee, livreur=livreur)

            # Récupérez toutes les commandes de la tournée avec les détails des articles
            commandes_tournee = Commande.objects.filter(tournee=tournee)
            commandes_data = []

            for commande in commandes_tournee:
                version_finale = Commande.objects.filter(id_commande=commande.id_commande, default=True).first()

                if version_finale:
                    articles_commande = [{
                        'id_article': caisse_commande.caisse.article.id_article,
                        'nom_article': caisse_commande.caisse.article.nom,
                        'nombre_articles': caisse_commande.caisse.nbr_articles,
                        'taille_article': caisse_commande.caisse.article.taille,
                        'quantite_caisse': float(caisse_commande.nbr_caisses),
                        'quantite_unite': int(caisse_commande.unite),
                    } for caisse_commande in Caisse_commande.objects.filter(commande=version_finale)]

                    commande_data = {
                        'id_commande': version_finale.id_commande,
                        'client': version_finale.client.name,
                        'default': version_finale.default,
                        'est_modifie': version_finale.est_modifie,
                        'articles': articles_commande,
                    }
                else:
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
                        'default': commande.default,
                        'est_modifie': commande.est_modifie,
                        'articles': articles_commande,
                    }

                commandes_data.append(commande_data)
        else:
            # Si l'utilisateur est un administrateur, permettez l'accès à toutes les tournées
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee)

            # Récupérez toutes les commandes de la tournée avec les détails des articles
            commandes_tournee = Commande.objects.filter(tournee=tournee)
            commandes_data = []

            for commande in commandes_tournee:
                version_modifiee = Commande.objects.filter(id_commande=commande.id_commande, default=True).first()

                if version_modifiee:
                    articles_commande = [{
                        'id_article': caisse_commande.caisse.article.id_article,
                        'nom_article': caisse_commande.caisse.article.nom,
                        'nombre_articles': caisse_commande.caisse.nbr_articles,
                        'taille_article': caisse_commande.caisse.article.taille,
                        'quantite_caisse': float(caisse_commande.nbr_caisses),
                        'quantite_unite': int(caisse_commande.unite),
                    } for caisse_commande in Caisse_commande.objects.filter(commande=version_modifiee)]

                    commande_data = {
                        'id_commande': version_modifiee.id_commande,
                        'client': version_modifiee.client.name,
                        'default': version_modifiee.default,
                        'est_modifie': version_modifiee.est_modifie,
                        'articles': articles_commande,
                    }
                else:
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
                        'default': commande.default,
                        'est_modifie': commande.est_modifie,
                        'articles': articles_commande,
                    }

                commandes_data.append(commande_data)

        return HttpResponse(json.dumps(commandes_data), content_type='application/json')
    except Exception as e:
        return JsonResponse({'error': str(e)})

