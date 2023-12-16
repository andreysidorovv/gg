from django.contrib import admin
from django.utils.html import format_html
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from import_export.widgets import ForeignKeyWidget
from rest_framework.reverse import reverse
from simple_history.admin import SimpleHistoryAdmin

from discounts.models import Store, PromoCode, Category


class StoreResource(resources.ModelResource):

    class Meta:
        model = Store


class PromocodeResource(resources.ModelResource):
    store = fields.Field(
        column_name='store',
        attribute='store',
        widget=ForeignKeyWidget(Store, field='name'))
    class Meta:
        model = PromoCode

    def dehydrate_is_active(self, promocode):
        is_active = 'Yes' if promocode.is_active else 'No'
        return f"{is_active}"



class PromoCodeInline(admin.TabularInline):
    model = PromoCode
    extra = 1

class StoreAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = StoreResource
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'description'),
        }),
        ('Category', {
            'classes': ('collapse',),
            'fields': ('category',),
        }),
    )
    inlines = [PromoCodeInline]


    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


class PromocodeAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = PromocodeResource
    list_display = ('code', 'discount_percent', 'expiration_date', 'is_active', 'store_link')

    list_filter = ('store', 'expiration_date', 'is_active')
    fields = ('code', 'discount_percent', 'expiration_date', 'is_active', 'store', 'likes', 'dislikes')

    def store_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse('admin:discounts_store_change', args=[obj.store.id]),
                           obj.store.name)

    store_link.short_description = 'Store'

    def get_export_queryset(self, request):
        return PromoCode.objects.filter(is_active=True)

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]



admin.site.register(Store, StoreAdmin)
admin.site.register(PromoCode, PromocodeAdmin)
admin.site.register(Category)

