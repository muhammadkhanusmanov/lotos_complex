from django.contrib import admin
from .models import *

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'price_per_unit')
    search_fields = ('name',)
    list_filter = ('unit',)



@admin.register(ProductIngredient)
class ProductIngredientAdmin(admin.ModelAdmin):
    list_display = ('product', 'ingredient', 'quantity')
    list_filter = ('product', 'ingredient')
    # Mahsulot va masalliqlarni qo'shish uchun inline admin qo'shamiz
    raw_id_fields = ('product', 'ingredient')

class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1
    raw_id_fields = ('ingredient',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    inlines = [ProductIngredientInline]  # Inline admin qo'shildi

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_user_id', 'customer_name', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'telegram_user_id')
    date_hierarchy = 'created_at'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'total_price')
    list_filter = ('product',)

@admin.register(IngredientCalculation)
class IngredientCalculationAdmin(admin.ModelAdmin):
    list_display = ('date', 'ingredient', 'required_quantity', 'status')
    list_filter = ('date', 'status', 'ingredient')
    search_fields = ('ingredient__name',)