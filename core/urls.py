from django.urls import path
from .views import *
from django.conf.urls.i18n import i18n_patterns

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<category>/', get_by_category, name='get_by_category'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummary.as_view(), name='order_summary'),
    path('product/<slug>/', ProductView.as_view(), name='product'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
    path('request_refund/', RequestRefundView.as_view(), name='request_refund'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('adjust_quantity/<slug>', adjust_quantity, name='adjust_quantity'),
    path('decrease_quantity/<slug>', decrease_quantity, name='decrease_quantity')

]