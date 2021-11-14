from django.contrib import admin
from .models import Bookstbl,Adminstbl,Userstbl
# Register your models here.

admin.site.register(Bookstbl)
admin.site.register(Adminstbl)
admin.site.register(Userstbl)