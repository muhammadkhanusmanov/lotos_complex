from django.urls import path
from . import views

urlpatterns = [
    # Mahsulotlar uchun endpointlar
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Buyurtmalar uchun endpointlar
    path('orders/', views.OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Masalliqlar hisobi uchun endpointlar
    path('ingredients/calculations/', views.IngredientCalculationView.as_view(), name='ingredient-calculations'),
    path('ingredients/calculations/daily/', views.DailyIngredientCalculationView.as_view(), name='daily-calculations'),
    
    # Ingredient endpointlari
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient-list'),
    path('ingredients/create/', views.IngredientCreateView.as_view(), name='ingredient-create'),
    
    # Product endpointlari
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
] 