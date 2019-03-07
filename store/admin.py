from django.contrib import admin
from .models import GUser, Items, Temp, Cart, Order, Order_Final, SUser

class Guser_Admin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "name",
        "dob",
        "sex",
        "phone",
        "address",
        "email",
    )

class Suser_Admin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "name",
        "dob",
        "sex",
        "phone",
        "address",
        "email",
    )

class Item_Admin(admin.ModelAdmin):
    list_display = (
        "item_id",
        "item_name",
        "stock",
        "price",
    )

class Item_Order(admin.ModelAdmin):
    list_display = (
        "order_id",
        "time_stamp",
        "item_name",
        "quantity",
        "price",
    )

class Item_Order_Final(admin.ModelAdmin):
    list_display = (
        "uid",
    )
admin.site.site_header="GSTORE"
admin.site.site_title="GSTORE"

admin.site.register(SUser, Suser_Admin)
admin.site.register(GUser, Guser_Admin)
admin.site.register(Items, Item_Admin)
admin.site.register(Order_Final,Item_Order_Final)
admin.site.register(Order, Item_Order)
admin.site.register(Cart)
admin.site.register(Temp)



