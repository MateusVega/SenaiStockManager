from django.contrib import admin
from .models import mecanica, eletrica, eletronica

admin.site.register(mecanica)
admin.site.register(eletrica)
admin.site.register(eletronica)