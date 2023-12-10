from django.urls import path

from .views.CommandeView import create_commande
from .views.CommandeView import get_commande
from .views.CommandeView import get_commandes
from .views.CommandeView import update_commande
from .views.CommandeView import commande_livre


from .views.LoginView import login
from .views.LoginView import getAll
from .views.LoginView import create_user
from .views.LoginView import logout_user
from .views.LoginView import load_user_data

#from .views.LoginView import connected_users

from .views.ClientView import create_client
from .views.ClientView import delete_client
from .views.ClientView import update_client


from .views.TourneeView import assigner_tournee
from .views.TourneeView import get_all_tournees
from .views.TourneeView import get_commandes_tournee
from .views.TourneeView import get_details_commandes_tournee



urlpatterns = [
    path('getOne/<commande_id>', get_commande, name="get_commande"),
    path('getAll', get_commandes, name="get_commandes"),
    path('create_commande', create_commande, name='create_commande'),
    path('update_commande/<commande_id>', update_commande, name='update_commande'),
    path('commande_livre/<commande_id>', commande_livre, name='commande livre'),

    path('loginUser', login , name='login_user'),
    path('getAllUsers', getAll, name='readall'),
    path('create', create_user, name='create_user'),
    path('logout/<str:token>', logout_user , name="logout"),
    path('loadUserData', load_user_data , name="create client"),
    #path('get_users_connected', connected_users , name="get_users_connected"),
    
    path('create_client', create_client , name="create client"),
    path('delete_client/<id_client>', delete_client , name="delete client"),
    path('update_client/<id_client>', update_client , name="update client"),

    path('assigner_tournee/<id_tournee>', assigner_tournee , name="assigner_tournee"),
    path('get_all_tournee', get_all_tournees , name="get all tournee"),
    path('get_commandes_from_tournee/<id_tournee>', get_commandes_tournee, name="get_commandes_tournee"),
    path('<int:id_tournee>/commandes/details', get_details_commandes_tournee, name='get_details_commandes_tournee'),

    ###path('delete/<int:user_id/', delete_user, name='delete_user'),

]
