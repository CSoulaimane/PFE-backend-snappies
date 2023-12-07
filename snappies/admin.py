from django.contrib import admin

from .models import Commande
from .models import User


admin.site.register(Commande)
admin.site.register(User)
