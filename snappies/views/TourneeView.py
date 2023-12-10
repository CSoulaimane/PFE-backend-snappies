
import json
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import  Caisse_commande, Commande, Tournee, User
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
            tournees_data = [{'id': tourne.id_tournee, 'livreur': tourne.livreur.username ,'nom': tourne.nom } for tourne in tournees]
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
def get_tournees_livreur(request, livreur_id):
    try:
        user = request.user
        if not user.is_admin:
            livreur = get_object_or_404(User, id_user=livreur_id, is_admin=False)

            tournees = Tournee.objects.filter(livreur=livreur)
            tournees_data = [{
                'id de la tournee': tournee.id_tournee,
                'livreur': tournee.livreur.username,
                'nom': tournee.nom,
                # Ajoutez d'autres champs de la tournée selon vos besoins
            } for tournee in tournees]

            return HttpResponse(json.dumps(tournees_data), content_type='application/json')
        else:
            return JsonResponse({'error': 'Only non-admin users (livreurs) can access this endpoint'})
    except Exception as e:
        return JsonResponse({'error': str(e)})    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_commandes_tournee(request, id_tournee):
    try:
        user = request.user
        if not user.is_admin:
            livreur = user  # Utilisez l'utilisateur authentifié comme livreur

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
            return JsonResponse({'error': 'Only non-admin users (livreurs) can access this endpoint'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_details_commandes_tournee(request, id_tournee):
    try:
        user = request.user
        if not user.is_admin:
            livreur = user  # Utilisez l'utilisateur authentifié comme livreur

            # Vérifiez si la tournée appartient au livreur
            tournee = get_object_or_404(Tournee, id_tournee=id_tournee, livreur=livreur)

            # Récupérez toutes les commandes de la tournée avec les détails des articles
            commandes_tournee = Commande.objects.filter(tournee=tournee)
            commandes_data = []

            for commande in commandes_tournee:
                articles_commande = [{
                    'id_article': caisse_commande.caisse.article.id_article,
                    'nom_article': caisse_commande.caisse.article.nom,
                    'nombre_articles' : caisse_commande.caisse.nbr_articles,
                    'taille_article': caisse_commande.caisse.article.taille,
                    'quantite_caisse': float(caisse_commande.nbr_caisse),
                    'quantite_unite':  int(caisse_commande.unite),
                } for caisse_commande in Caisse_commande.objects.filter(commande=commande)]

                commande_data = {
                    'id_commande': commande.id_commande,
                    'client': commande.client.name,
                    'default': commande.default,
                    'est_modifie': commande.est_modifie,
                    'articles': articles_commande,
                    # Ajoutez d'autres champs de la commande selon vos besoins
                }

                commandes_data.append(commande_data)

            return HttpResponse(json.dumps(commandes_data), content_type='application/json')
        else:
            return JsonResponse({'error': 'Only non-admin users (livreurs) can access this endpoint'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
