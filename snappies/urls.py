from django.urls import path

from .views.CommandeView import create_commande
from .views.CommandeView import get_commande
from .views.CommandeView import get_commandes_tournee_admin,get_commandes_tournee_modifie_ou_non
from .views.CommandeView import update_commande_admin,update_livraison
from .views.CommandeView import commande_livre,update_est_livre
from .views.CommandeView import get_admin_commandes
from .views.CommandeView import get_livreur_commandes

from .views.LoginView import login,delete_user
from .views.LoginView import getAll
from .views.LoginView import create_user
from .views.LoginView import logout_user
from .views.LoginView import load_user_data
from .views.LoginView import get_all_livreurs
from .views.LoginView import delete_livreur
from .views.LoginView import update_livreur
from .views.LoginView import delete_user
from .views.LoginView import get_user
from .views.LoginView import create_livreur

#from .views.LoginView import connected_users

from .views.ClientView import create_client
from .views.ClientView import delete_client
from .views.ClientView import update_client
from .views.ClientView import get_all_clients_free
from .views.ClientView import get_client

from .views.TourneeView import assigner_tournee
from .views.TourneeView import get_all_tournees
from .views.TourneeView import get_commandes_tournee
from .views.TourneeView import get_details_commandes_tournee
from .views.TourneeView import get_tournees_livreur
from .views.TourneeView import creer_tournee


from .views.ArticleView import get_all_articles
from .views.ArticleView import create_article
from .views.ArticleView import delete_article
from .views.ArticleView import update_article


urlpatterns = [
    path('getOne/<commande_id>', get_commande, name="get_commande"),
    path('create_commande', create_commande, name='create_commande'),
    path('update_commande_admin/<id_commande>', update_commande_admin, name='update_commande_admin'),
    path('commande_livre/<commande_id>', commande_livre, name='commande livre'),
    path('get_commandes_tournee_admin/<id_tournee>', get_commandes_tournee_admin, name='get_commandes_tournee_admin'),
    path('get_commandes_tournee_modifie_ou_non/<id_tournee>', get_commandes_tournee_modifie_ou_non, name='get_commandes_tournee_modifie_ou_non'),
    path('update_livraison/<id_commande>', update_livraison, name='ud'),
    path('update_est_livre', update_est_livre, name='est livre'),


    
    path('loginUser', login , name='login_user'),
    path('getAllUsers', getAll, name='readall'),
    path('create', create_user, name='create_user'),
    path('delete_user/<id_user>', delete_user, name='delete_user'),
    path('logout/<str:token>', logout_user , name="logout"),
    path('loadUserData', load_user_data , name="create client"),
    path('getAllLivreurs', get_all_livreurs , name="get_all_livreurs"),
    path('delete_livreur/<id_user>', delete_livreur, name="delete_livreur"),
    path('update_user/<id_user>', update_livreur, name="update_livreur"),
    path('delete_user/<id_user>', delete_user, name="delete_user"),
    path('get_user/<id_user>', get_user, name="get_user"),
    path('create_livreur', create_livreur, name="create livreur"),

    #path('get_users_connected', connected_users , name="get_users_connected"),
    
    path('create_client', create_client , name="create client"),
    path('delete_client/<id_client>', delete_client , name="delete client"),
    path('update_client/<id_client>', update_client , name="update client"),
    path('get_all_clients_free', get_all_clients_free , name="get_all_clients_free"),
    path('get_client/<int:id_client>', get_client , name="get_client"),

    path('assigner_tournee/<id_tournee>', assigner_tournee , name="assigner_tournee"),
    path('get_all_tournee', get_all_tournees , name="get all tournee"),
    path('get_commandes_from_tournee/<id_tournee>', get_commandes_tournee, name="get_commandes_tournee"),
    path('<int:id_tournee>/commandes/details', get_details_commandes_tournee, name='get_details_commandes_tournee'),
    path('get_tournees_livreur/<username_livreur>', get_tournees_livreur, name='get_tournees_livreur'),
    path('creer_tournee', creer_tournee, name='creer_tournee'),


    path('get_all_articles',get_all_articles, name ='get all article'),
    path('create_article',create_article, name ='create article'),
    path('update_article/<id>',update_article, name ='update article'),
    path('delete_article/<id>',delete_article, name ='delete article'),

    ###path('delete/<int:user_id/', delete_user, name='delete_user'),

]
