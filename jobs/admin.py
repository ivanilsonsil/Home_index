from django.contrib import admin
from .models import Referencias, Jobs #import models criados


 # registrando  meus models no admin

admin.site.register(Jobs)
admin.site.register(Referencias)
