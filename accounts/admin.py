from django.contrib import admin
from .models import CustomUser,Item,CartItem,UserProfile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(UserProfile)

