from django.contrib import admin
from .models import Product,Sales,Csv

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","description","unit_price",]
    fields = ["title","description","unit_price","image"]
    search_fields = ["title"]

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['product','salesmen','sales_date','qty']
    fields = ['product','salesmen','sales_date','qty']
    list_select_related = ['product','salesmen']

@admin.register(Csv)    
class CsvAdmin(admin.ModelAdmin):
    list_display = ['filename','status','upload_at']
    fields = ['filename','status','upload_at']
    search_fields =["filename"]