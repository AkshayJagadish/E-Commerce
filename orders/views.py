from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm
from .models import Product, OrderProduct, Order, ShippingAddress, ReqInfo
from django.views.generic import ListView, DetailView, View
from django.core.files.storage import FileSystemStorage


class CheckoutView(View):
    def get(self, *args, **kwargs):
        #form
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, order_status=0)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, order_status=0)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                zip = form.cleaned_data.get('zip')

                shipping_address = ShippingAddress(
                    user=self.request.user,
                    email=email,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    zip=zip
                )

                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                # order.ordered = True
                order.order_status = 2
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect('orders:home')
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect('orders:order-summary')
        messages.warning(self.request, 'Failed Checkout')
        return redirect('orders:checkout')


class HomeView(ListView):
    model = Product
    template_name = 'home.html'


# displays list of all OrderProducts within an order
class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, order_status=0)  # we get the list of OrderProducts
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect('orders:home')


class ItemDetailView(DetailView):
    model = Product
    template_name = 'product.html'


@login_required # ensures the user is authorized to access this page
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderProduct.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, order_status=0)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The quantity was updated.")
            return redirect("orders:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("orders:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("orders:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        order_status=0
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            # deleted the order item from the cart if it exists
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect('orders:order-summary')
        else:
            # add a message saying thr user does not have an order
            messages.info(request, "This item was not in your cart.")
            return redirect('orders:product', slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('orders:order-summary', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        order_status=0
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity == 1:
                order.items.remove(order_item)

            else:
                order_item.quantity -= 1
                order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('orders:order-summary')
        else:
            # add a message saying thr user does not have an order
            messages.info(request, "This item was not in your cart.")
            return redirect('orders:product', slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('orders:product', slug=slug)


def about_us(request):
    return render(request, 'about_us.html')


@login_required
def myorders(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user)
    req_info = ReqInfo.objects.get(user=request.user)
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(filename, uploaded_file_url)
        rq = ReqInfo.objects.get(user=request.user)
        rq.my_pp = filename
        rq.save()


        response = render(request, 'myorders.html', {'orders': orders, 'req_info': rq })
        return response

    response = render(request, 'myorders.html', {'orders': orders, 'req_info': req_info })
    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.now()
        response.set_cookie('last_visit', str(datetime.now()))

    else:
        response.set_cookie('last_visit', datetime.now())

    return response