from django.contrib import admin

# Register your models here.

from.models import Utente, Transizione

from django.contrib.auth.models import User
from django.contrib.auth.models import Group


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Utente)
admin.site.register(Transizione)