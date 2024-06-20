from django.contrib import admin

from .models import Collaborateur, Role

admin.site.register(Collaborateur)
admin.site.register(Role)
