from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def user_signed_up(request, user, sociallogin = None, **kwargs):
    ReqInfo.objects.create(user=user)


def validate_stock(value):
    if value < 0 or value > 1000:
        raise ValidationError(
            _('%(value)s is not a valid stock option'),
            params={'value': value},
        )


# category class defined for class products
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=100, blank=False, null=False, default='')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


# class product with some fields
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=50, validators=[validate_stock])
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True, default='')
    slug = models.SlugField()
    measure = models.CharField(max_length=20)

# default value that is displayed when this object is called
    def __str__(self):
        return self.name

# returns the absolute url for the particular slug
    def get_absolute_url(self):
        return reverse("orders:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("orders:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("orders:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # user uses all auth
    ordered = models.BooleanField(default=False) # to know if an order has been placed or not
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    items = models.ManyToManyField(OrderProduct)  # an order can have many items in it
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ORDER_STATUS_CHOICE = [(0, 'Order Pending'),  # list of order state
                           (1, 'Order Cancelled'),
                           (2, 'Order Placed'),
                           (3, 'Order Shipped'),
                           (4, 'Order Delivered')]

    order_status = models.IntegerField(default=0, choices=ORDER_STATUS_CHOICE)  # default order state is 0 which is pending
    ordered_date = models.DateField(auto_now_add=True)
    shipping_address = models.ForeignKey(
        'ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class ReqInfo(models.Model):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    my_pp = models.ImageField(upload_to='profile_picture/', blank=True, null=True, default='profile_picture/df.jpg')
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return self.user.username + ": " + str(self.my_pp)