from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
from .forms import CsvModelFrom

# Register your models here.
@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display= ["description","discount"]
    search_fields = ['description']

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    #nlines = [ProductImageInline]
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    #list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

    # class Media:
    #     css = {
    #         'all': ['store/styles.css']
    #     }


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:sales_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(models.Sales)
class SalesAdmin(admin.ModelAdmin):

    list_display = ['product','salesmen','sales_date','qty']
    fields = ['product','salesmen','qty']
    list_select_related = ['product','salesmen']

    
@admin.register(models.Csv)    
class CsvAdmin(admin.ModelAdmin):
    list_display = ['filename','status']
    fields = ['filename']
    search_fields =["filename"]
    
    form = CsvModelFrom