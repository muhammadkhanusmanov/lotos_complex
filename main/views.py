from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils import timezone
from .models import Product, Order, OrderItem, IngredientCalculation, Ingredient, ProductIngredient
from .serializers import (
    ProductSerializer, 
    OrderSerializer, 
    OrderCreateSerializer,
    IngredientCalculationSerializer,
    IngredientSerializer,
    ProductCreateSerializer,
    ProductDetailSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser
import json

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # Buyurtma yaratilgandan so'ng masalliqlarni hisoblash
        self.calculate_ingredients(order)

    def calculate_ingredients(self, order):
        # Har bir buyurtma elementi uchun masalliqlarni hisoblash
        for item in order.items.all():
            product = item.product
            quantity = item.quantity
            
            # Mahsulot uchun kerakli masalliqlarni hisoblash
            for product_ingredient in product.product_ingredients.all():
                required_quantity = product_ingredient.quantity * quantity
                
                # Kunlik hisobga qo'shish
                calculation, created = IngredientCalculation.objects.get_or_create(
                    date=timezone.now().date(),
                    ingredient=product_ingredient.ingredient,
                    defaults={'required_quantity': 0}
                )
                calculation.required_quantity += required_quantity
                calculation.save()

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class IngredientCalculationView(APIView):
    def get(self, request):
        # Sanani olish (default: bugun)
        date = request.query_params.get('date', timezone.now().date())
        
        calculations = IngredientCalculation.objects.filter(date=date)
        serializer = IngredientCalculationSerializer(calculations, many=True)
        
        return Response(serializer.data)

class DailyIngredientCalculationView(APIView):
    def get(self, request):
        # Kunlik masalliqlar hisobi
        start_date = request.query_params.get('start_date', timezone.now().date())
        end_date = request.query_params.get('end_date', start_date)
        
        calculations = IngredientCalculation.objects.filter(
            date__range=[start_date, end_date]
        ).values(
            'ingredient__name', 
            'ingredient__unit'
        ).annotate(
            total_quantity=Sum('required_quantity')
        )
        
        return Response(calculations)

class IngredientCreateView(generics.CreateAPIView):
    serializer_class = IngredientSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IngredientListView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        product_data = request.data.copy()
        ingredients_data = json.loads(request.data.get('ingredients', '[]'))
        
        # Mahsulot yaratish
        product_serializer = ProductCreateSerializer(data=product_data)
        if product_serializer.is_valid():
            product = product_serializer.save()
            
            # Ingredientlarni qo'shish
            for ingredient_data in ingredients_data:
                ProductIngredient.objects.create(
                    product=product,
                    ingredient_id=ingredient_data['ingredient_id'],
                    quantity=ingredient_data['quantity']
                )
            
            # To'liq ma'lumotni qaytarish
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product_data = request.data.copy()
        ingredients_data = json.loads(request.data.get('ingredients', '[]'))
        
        # Mahsulot yangilash
        product_serializer = ProductCreateSerializer(product, data=product_data, partial=True)
        if product_serializer.is_valid():
            product = product_serializer.save()
            
            # Eski ingredientlarni o'chirish
            product.product_ingredients.all().delete()
            
            # Yangi ingredientlarni qo'shish
            for ingredient_data in ingredients_data:
                ProductIngredient.objects.create(
                    product=product,
                    ingredient_id=ingredient_data['ingredient_id'],
                    quantity=ingredient_data['quantity']
                )
            
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
