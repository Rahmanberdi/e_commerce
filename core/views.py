from django.shortcuts import render, get_object_or_404
from .models import *
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.utils.translation import gettext as _

# Create your views here.
import random, string

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase+string.digits, k=20))

class HomeView(generic.ListView):
    model = Item
    extra_context = {
        'category':'All'
    }
    paginate_by = 10
    context_object_name = 'items'
    template_name = 'home.html'


class OrderSummary(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, _("You do not have an active order"))
            return redirect('core:home')


class CheckoutView(generic.View):
    def get(self, *args, **kwargs):
        #form
        form = CheckoutForm()
        coupon_form = CouponForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        order.total_amount = order.get_total()
        if order.coupon:
            order.total_amount -= order.coupon.amount
        order.save()
        context = {
            'form':form,
            'coupon_form':coupon_form,
            'order':order,
        }
        return render(self.request,"checkout.html",context)

    def post(self, *args, **kwargs):
        form =CheckoutForm(self.request.POST or None)
        coupon_form = CouponForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surname')
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                velayat = form.cleaned_data.get('velayat')
                phone_number = form.cleaned_data.get('phonenumber')
                save_info = form.cleaned_data.get('save_info')
                billing_address = BillingAddress(
                    user=self.request.user,
                    name=name,
                    surname=surname,
                    velayat=velayat,
                    phonenumber=phone_number,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                )
                billing_address.save()
                order.billing_address=billing_address
                order.ref_code = create_ref_code()
                order.ordered = True
                order.save()
                for item in order.items.all():
                    item.ordered = True
                    item.save()
                messages.success(self.request,_('Your items were purchased successfully'))
                return redirect('core:home')

            if coupon_form.is_valid():
                coupon = coupon_form.cleaned_data.get('coupon')
                if Coupon.objects.filter(code=coupon).exists():
                    coupon = Coupon.objects.get(code=coupon)
                    if order.coupon:
                        if coupon.amount > order.coupon.amount:
                            order.coupon = coupon
                            messages.success(self.request, _("Your coupon was added successfully"))
                        else:
                            messages.info(self.request, _("Your old coupons amount was much bigger"))
                    else:
                        order.coupon = coupon
                        messages.success(self.request, _("Your coupon was added successfully"))
                    order.save()
                else:
                    messages.warning(self.request, _("Your coupon doesn't exists or it is out of date"))
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, _("You do not have an active order"))
            return redirect("core:home")

class PaymentView(generic.View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')


class ProductView(generic.DetailView):
    model = Item
    template_name = 'product.html'


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, _("This item was updated"))
            return redirect("core:product", slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, _("This item was added to your cart"))
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.save()
        order.items.add(order_item)
        messages.info(request, _("This item was added to your cart"))
        return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, _("This item was removed from your cart"))
            return redirect('core:order_summary')
        else:
            messages.info(request, _("This item was not in your cart"))
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, _("You don't have an existing order"))
        return redirect('core:product', slug=slug)


def adjust_quantity(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.get(user=request.user, ordered=False)
    # check if the order item is in the order
    order_item = order.items.get(
        item=item,
        ordered=False,
    )

    order_item.quantity += 1
    order_item.save()
    return redirect("core:order_summary")

def decrease_quantity(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.get(user=request.user, ordered=False)
    # check if the order item is in the order
    order_item = order.items.get(
        item=item,
        ordered=False,
    )
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order.items.remove(order_item)
        order_item.delete()
    return redirect("core:order_summary")


class RequestRefundView(generic.View):
    def get(self,*args,**kwargs):
        form = RefundForm()
        context = {
            'form':form
        }
        return render(self.request, 'request_refund.html',context=context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data['ref_code']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']

            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = RefundModel()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, _("Your request was received"))
                return redirect('/')
            except ObjectDoesNotExist:
                messages.info(self.request, _("This order does not exist"))
                return redirect('/')

def get_by_category(request, category):
    context = {
        'items': Item.objects.filter(category=category),
        'category':category
    }
    return render(request, 'home.html', context)
