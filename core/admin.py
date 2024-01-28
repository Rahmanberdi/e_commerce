from django.contrib import admin
from .models import *
# Register your models here.

def make_refund_accepted (modeladmin, request, queryset):
    queryset.update(refund_accepted=True)

make_refund_accepted.short_description = 'Update orders to refund accepted'

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered',
        'being_delivered',
        'received',
        'refund_requested',
        'refund_granted',
        'user',
        'billing_address',
        'coupon',
                    ]
    list_display_links = [
        'user',
        'billing_address',
        'coupon',
    ]
    list_filter = ['ordered','being_delivered','received','refund_requested','refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
admin.site.register(RefundModel)
