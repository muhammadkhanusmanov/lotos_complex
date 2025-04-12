from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pcs', 'Dona'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nomi")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="Oʻlchov birligi")
    price_per_unit = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Narxi (birlik uchun)",
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Masalliq"
        verbose_name_plural = "Masalliqlar"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_unit_display()})"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Narxi",
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Rasm")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    ingredients = models.ManyToManyField(
        Ingredient,
        through='ProductIngredient',
        related_name='products',
        verbose_name="Masalliqlar"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProductIngredient(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='product_ingredients',
        verbose_name="Mahsulot"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_products',
        verbose_name="Masalliq"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Miqdori",
        validators=[MinValueValidator(0.001)]
    )
    
    class Meta:
        verbose_name = "Mahsulot masalliqi"
        verbose_name_plural = "Mahsulot masalliqlari"
        unique_together = ['product', 'ingredient']
    
    def __str__(self):
        return f"{self.product} - {self.ingredient}: {self.quantity} {self.ingredient.unit}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('accepted', 'Qabul qilindi'),
        ('preparing', 'Tayyorlanmoqda'),
        ('ready', 'Tayyor'),
        ('completed', 'Yakunlandi'),
        ('cancelled', 'Bekor qilindi'),
    ]
    
    telegram_user_id = models.BigIntegerField(verbose_name="Telegram foydalanuvchi ID")
    customer_name = models.CharField(max_length=100, blank=True, verbose_name="Mijoz ismi")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefon raqam")
    delivery_date = models.DateField(
        verbose_name="Yetkazib berish sanasi",
        default=timezone.now
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Holati"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Umumiy summa",
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    notes = models.TextField(blank=True, verbose_name="Qo'shimcha izohlar")
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.id} - {self.customer_name or self.telegram_user_id} - {self.get_status_display()}"
    
    def update_total(self):
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Buyurtma"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name="Mahsulot"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdor")
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Birlik narxi",
        validators=[MinValueValidator(0)]
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Umumiy narx",
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"
    
    def __str__(self):
        return f"{self.order} - {self.product} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()


class IngredientCalculation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('prepared', 'Tayyorlangan'),
        ('purchased', 'Sotib olingan'),
    ]
    
    date = models.DateField(verbose_name="Sana")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='calculations',
        verbose_name="Masalliq"
    )
    required_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Kerakli miqdor",
        validators=[MinValueValidator(0.001)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Holati"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Masalliq hisobi"
        verbose_name_plural = "Masalliq hisoblari"
        unique_together = ['date', 'ingredient']
        ordering = ['date', 'ingredient']
    
    def __str__(self):
        return f"{self.date} - {self.ingredient}: {self.required_quantity} {self.ingredient.unit}"