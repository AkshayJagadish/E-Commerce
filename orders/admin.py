from django.contrib import admin
from .models import Product, Category, Order, OrderProduct, ShippingAddress, ReqInfo
from django.db.models import F
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_status']


def add_stock(modeladmin, request, queryset):
    queryset.update(stock=F('stock')+50)
add_stock.short_description = "Add 50 items to stock"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available']
    actions = [add_stock]


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_first_name', 'get_last_name', 'get_interested_in', 'city']


    def get_first_name(self, ReqInfo):
        return ReqInfo.user.first_name
    get_first_name.short_description = "First Name"


    def get_last_name(self, ReqInfo):
        return ReqInfo.user.last_name
    get_last_name.short_description = "Last Name"

    def get_interested_in(self, ReqInfo):
        return ", ".join([item.name for item in ReqInfo.interested_in.all()])
    get_interested_in.short_description = "Interested in"


admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(ReqInfo, ClientAdmin)
