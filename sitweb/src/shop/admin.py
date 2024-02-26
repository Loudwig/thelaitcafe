from django.contrib import admin
from .models import Capsule,Transaction,CustomUser

admin.site.register(Capsule)
admin.site.register(Transaction)
admin.site.register(CustomUser)
