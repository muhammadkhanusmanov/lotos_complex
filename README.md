# Lotos Complex API Documentation

Bu API Lotos Complex loyihasi uchun backend xizmatlarini taqdim etadi. API orqali mahsulotlar, buyurtmalar va masalliqlar bilan ishlash mumkin.

## API Endpoints

### Mahsulotlar (Products)

#### 1. Mahsulotlar ro'yxatini olish
```http
GET /api/products/
```
**Response:**
```json
[
    {
        "id": 1,
        "name": "Osh",
        "description": "Palov",
        "price": "50000.00",
        "image": "/media/products/osh.jpg",
        "is_active": true
    }
]
```

#### 2. Mahsulot ma'lumotlarini olish
```http
GET /api/products/{id}/
```
**Response:**
```json
{
    "id": 1,
    "name": "Osh",
    "description": "Palov",
    "price": "50000.00",
    "image": "/media/products/osh.jpg",
    "is_active": true,
    "ingredients": [
        {
            "ingredient": 1,
            "ingredient_name": "Guruch",
            "unit": "kg",
            "quantity": 0.2
        }
    ]
}
```

#### 3. Yangi mahsulot yaratish
```http
POST /api/products/create/
```
**Request:**
```json
{
    "name": "Osh",
    "description": "Palov",
    "price": "50000.00",
    "is_active": true,
    "ingredients": [
        {
            "ingredient_id": 1,
            "quantity": 0.2
        }
    ]
}
```
**Response:** 201 Created

#### 4. Mahsulotni yangilash
```http
PATCH /api/products/{id}/update/
```
**Request:**
```json
{
    "name": "Yangilangan Osh",
    "price": "55000.00",
    "ingredients": [
        {
            "ingredient_id": 1,
            "quantity": 0.25
        }
    ]
}
```
**Response:** 200 OK

### Buyurtmalar (Orders)

#### 1. Yangi buyurtma yaratish
```http
POST /api/orders/
```
**Request:**
```json
{
    "telegram_user_id": 123456789,
    "customer_name": "John Doe",
    "phone_number": "+998901234567",
    "items": [
        {
            "product": 1,
            "quantity": 2
        }
    ]
}
```
**Response:**
```json
{
    "id": 1,
    "telegram_user_id": 123456789,
    "customer_name": "John Doe",
    "phone_number": "+998901234567",
    "status": "new",
    "total_amount": "100000.00",
    "items": [
        {
            "id": 1,
            "product": 1,
            "product_name": "Osh",
            "product_price": "50000.00",
            "quantity": 2,
            "unit_price": "50000.00",
            "total_price": "100000.00"
        }
    ]
}
```

#### 2. Buyurtma ma'lumotlarini olish
```http
GET /api/orders/{id}/
```
**Response:**
```json
{
    "id": 1,
    "telegram_user_id": 123456789,
    "customer_name": "John Doe",
    "phone_number": "+998901234567",
    "status": "new",
    "total_amount": "100000.00",
    "items": [...]
}
```

### Masalliqlar (Ingredients)

#### 1. Masalliqlar ro'yxatini olish
```http
GET /api/ingredients/
```
**Response:**
```json
[
    {
        "id": 1,
        "name": "Guruch",
        "unit": "kg",
        "price_per_unit": "15000.00",
        "description": "Lazer guruch"
    }
]
```

#### 2. Yangi masalliq yaratish
```http
POST /api/ingredients/create/
```
**Request:**
```json
{
    "name": "Guruch",
    "unit": "kg",
    "price_per_unit": "15000.00",
    "description": "Lazer guruch"
}
```
**Response:** 201 Created

### Masalliqlar hisobi (Ingredient Calculations)

#### 1. Kunlik masalliqlar hisobi
```http
GET /api/ingredients/calculations/?date=2024-04-10
```
**Response:**
```json
[
    {
        "date": "2024-04-10",
        "ingredient_name": "Guruch",
        "unit": "kg",
        "required_quantity": 5.5,
        "status": "pending"
    }
]
```

#### 2. Davr uchun masalliqlar hisobi
```http
GET /api/ingredients/calculations/daily/?start_date=2024-04-01&end_date=2024-04-10
```
**Response:**
```json
[
    {
        "ingredient_name": "Guruch",
        "unit": "kg",
        "total_quantity": 55.5
    }
]
```

## Status kodlari

- `200 OK` - So'rov muvaffaqiyatli bajarildi
- `201 Created` - Yangi resurs yaratildi
- `400 Bad Request` - So'rovda xatolik bor
- `404 Not Found` - So'ralgan resurs topilmadi
- `500 Internal Server Error` - Serverda xatolik yuz berdi

## Xavfsizlik

- API barcha so'rovlar uchun `Content-Type: application/json` headerini talab qiladi
- Fayl yuklash uchun `multipart/form-data` ishlatiladi
- CORS sozlamalari orqali faqat ruxsat berilgan domainlardan so'rovlar qabul qilinadi

## Test qilish

API ni test qilish uchun Swagger dokumentatsiyasidan foydalanishingiz mumkin:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`
- OpenAPI JSON: `/swagger.json`

## Eslatmalar

1. Barcha pul birliklari `decimal` formatida, 2 ta o'nlik son bilan
2. Sanalar ISO format (`YYYY-MM-DD`)da yuborilishi kerak
3. Rasmlar `jpg`, `png` formatida qabul qilinadi
4. Telegram user ID `BigInteger` formatida bo'lishi kerak