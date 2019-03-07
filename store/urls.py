from django.urls import path
from .views import User_Auth, Staff_Auth
from . import views

urlpatterns = [
    path("store/", views.store, name='store'),
    path("cart/", views.cart, name='cart'),
    path("about/", views.about, name='about'),
    path("adduser/", views.add_user, name='add_user'),
    path("changepwd/", views.user_change_pwd, name='changepwd'),
    path("logout/", views.log_out, name='logout'),
    path("confirm/", views.confirm, name='confirm'),
    path("", User_Auth.as_view(), name='home'),
    path("staff_auth/", Staff_Auth.as_view(), name='staff_auth'),
    path("update_items/", views.update_item, name='update_items'),
    path("item_add/", views.add_item, name='add_items'),
    path("orders/", views.orders, name='orders')
]