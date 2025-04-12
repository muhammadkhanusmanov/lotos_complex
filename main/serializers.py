from rest_framework import serializers
from .models import Product, Order, OrderItem, IngredientCalculation, Ingredient, ProductIngredient

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'telegram_user_id', 'customer_name', 'phone_number', 
                 'status', 'total_amount', 'items', 'created_at']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'telegram_user_id', 'customer_name', 'phone_number', 'items', 'status', 'total_amount']
        read_only_fields = ['id', 'status', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=product.price,
                total_price=product.price * item_data['quantity']
            )
        
        order.update_total()
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = OrderItemSerializer(instance.items.all(), many=True).data
        return representation

class IngredientCalculationSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name')
    unit = serializers.CharField(source='ingredient.unit')
    
    class Meta:
        model = IngredientCalculation
        fields = ['date', 'ingredient_name', 'unit', 'required_quantity', 'status']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'unit', 'price_per_unit', 'description']

class ProductIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    unit = serializers.CharField(source='ingredient.unit', read_only=True)
    
    class Meta:
        model = ProductIngredient
        fields = ['ingredient', 'ingredient_name', 'unit', 'quantity']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'is_active']

class ProductDetailSerializer(serializers.ModelSerializer):
    ingredients = ProductIngredientSerializer(source='product_ingredients', many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'is_active', 'ingredients'] 