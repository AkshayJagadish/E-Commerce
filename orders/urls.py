from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView, ItemDetailView, add_to_cart, remove_from_cart, OrderSummary,\
    remove_single_item_from_cart, CheckoutView, about_us, myorders

app_name = 'orders'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummary.as_view(), name='order-summary'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('myorders', myorders, name='myorders'),
    path('aboutus', about_us, name='aboutus')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
