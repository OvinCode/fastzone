from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.HomeView,name='home'),

    path('register/', views.RegisterUser,name='register-user'),
    path('login/', views.LoginUser,name='login-user'),
    path("logout/", views.LogoutUser, name='logout-user'),

    path('add-to-cart/<int:itemId>', views.add_to_cart, name='add_to_cart'),
    path('delete-to-cart/<int:itemId>', views.delete_to_cart, name='delete_to_cart'),
    
    path('cart/', views.cart_view, name='cart'),

    path('checkout/', views.cart_checkout, name='checkout'),

   
    path('place_order/', views.place_order, name='place_order'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
