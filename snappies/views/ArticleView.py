import json
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import  Article,Caisse_commande, Commande, Tournee, User,Caisse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_articles(request):
    try:
        user = request.user
        if user.is_admin:
            caisses = Caisse.objects.all()
            tournees_data = [{ 'id_caisse': c.id_caisse,'article': c.article.id_article, 'nom': c.article.nom ,'taille': c.article.taille,
                               'type': c.article.types, 'nbr_articles': c.nbr_articles } for c in caisses]
            return HttpResponse(json.dumps(tournees_data), content_type='application/json')
        else:
            return JsonResponse({'error': 'You are not authorized to create a commande'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_article(request):
    user = request.user
    if user.is_admin:
        data = json.loads(request.body)
        nom = data.get('nom')
        type = data.get('type')
        nbr_articles = data.get('nbr_articles')

        try: 
            article = Article.objects.get(nom=nom)
        except Article.DoesNotExist: 
            article = Article(types=type,nom=nom)
            article.save()

            article = Article.objects.get(nom=nom)

            if(type == 'C'):
                if(nbr_articles == 0):
                    article.delete()
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                caisse = Caisse(article=article,nbr_articles=nbr_articles)
            elif(type == 'U'):
                caisse = Caisse(article=article,nbr_articles=0)
            else:
                 article.delete()
                 return Response(status=status.HTTP_400_BAD_REQUEST)
            caisse.save()
            created_data = {'id_caisse': caisse.id_caisse,'id_article': caisse.article.id_article, 'nom': caisse.article.nom ,'taille': caisse.article.taille,
                                'type': caisse.article.types, 'nbr_articles': caisse.nbr_articles }
        
            return Response(created_data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
       

    

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_article(request, id):
    user = request.user
    if user.is_admin:
        try:
            article = Article.objects.get(id_article=id)
            caisse = Caisse.objects.get(article=article)
            caisse.delete()
            article.delete()
        except Article.DoesNotExist | Caisse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_article(request, id):
    user = request.user
    if user.is_admin:
        try:
            article = Article.objects.get(id_article=id)  
            caisse = Caisse.objects.get(article=article)

            data = json.loads(request.body)
            nom = data.get('nom')
            nbr_articles = data.get('nbr_articles')

            if(nom == ""):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if article.types == "C":
                article.nom = nom
                caisse.nbr_articles = nbr_articles
                caisse.save()
            else:
                article.nom = nom
            article.save()


        except Article.DoesNotExist | Caisse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)