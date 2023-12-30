from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.http import HttpResponse
from .serializers import ProductSerializer
import csv
from . import models
from .forms import CsvModelFrom
import simplejson as json


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
    actions = ['clear_inventory','csv_export','json_export']
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

    @admin.action(description='JSON Export')
    def json_export(self,request,queryset):
        meta = self.model._meta
        ps = ProductSerializer(queryset, many=True)
        response = HttpResponse(json.dumps(ps.data),content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename={}.json'.format(meta)

        return response
        
     

    @admin.action(description='CSV Export')
    def csv_export(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

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
    fields = ['filename','propertis']
    search_fields =["filename"]
    
    form = CsvModelFrom