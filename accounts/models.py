from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import  OneToOneField

# Create your models here.
class CustomUser(AbstractUser):

    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    # address = models.CharField(max_length=250, blank=True, null=True)
    # country = models.CharField(max_length=15, blank=True, null=True)
    # state = models.CharField(max_length=15, blank=True, null=True)
    # city = models.CharField(max_length=15, blank=True, null=True)
    # pin_code = models.CharField(max_length=6, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
   

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

class UserProfile(models.Model):
    user = OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True)
    # latitude = models.CharField(max_length=20, blank=True, null=True)
    # longitude = models.CharField(max_length=20, blank=True, null=True)
    # location = gismodels.PointField(blank=True, null=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'

    def __str__(self):
        return self.user.email

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(null=True, default="avatar.svg")



    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items')
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} - Quantity: {self.quantity}"

    @property
    def total_price(self):
        """
        Calculates the total price of the menu item based on the quantity.

        Returns:
            float: The total price of the menu item.

        """
        return self.menu_item.price * self.quantity
