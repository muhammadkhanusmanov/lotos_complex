import requests
import json
from datetime import datetime, timedelta
import os

BASE_URL = "https://lotoscomplexbc.pythonanywhere.com/api"

def test_all_endpoints():
    # 1. Mahsulotlar ro'yxatini olish
    print("\n1. Barcha mahsulotlar:")
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response)

    # 2. Ingredientlar ro'yxatini olish
    print("\n2. Barcha ingredientlar:")
    response = requests.get(f"{BASE_URL}/ingredients/")
    print_response(response)

    # 3. Barcha buyurtmalarni olish
    print("\n3. Barcha buyurtmalar:")
    response = requests.get(f"{BASE_URL}/orders/")
    print_response(response)

    # 4. Bugungi hisoblar
    print("\n4. Bugungi hisoblar:")
    today = datetime.now().date()
    response = requests.get(
        f"{BASE_URL}/ingredients/calculations/",
        params={'date': today.isoformat()}
    )
    print_response(response)

    # 5. Oxirgi 3 kunlik hisoblar
    print("\n5. Oxirgi 3 kunlik hisoblar:")
    three_days_ago = today - timedelta(days=3)
    response = requests.get(
        f"{BASE_URL}/ingredients/calculations/daily/",
        params={
            'start_date': three_days_ago.isoformat(),
            'end_date': today.isoformat()
        }
    )
    print_response(response)

def create_test_order():
    print("\nTest buyurtma yaratish:")
    # Ertangi sana uchun buyurtma
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    order_data = {
        "telegram_user_id": 123456789,
        "customer_name": "Test User",
        "phone_number": "+998901234567",
        "delivery_date": tomorrow.isoformat(),  # Sana qo'shildi
        "items": [
            {
                "product": 1,
                "quantity": 2
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/orders/",
        headers={'Content-Type': 'application/json'},
        json=order_data
    )
    print_response(response)

def create_product_ingredients():
    print("\nMahsulot ingredientlarini qo'shish:")
    data = {
        "name": "Osh",  # Mavjud mahsulot
        "ingredients": json.dumps([
            {
                "ingredient_id": 1,  # Sabzi
                "quantity": 0.3  # 300 gram
            },
            {
                "ingredient_id": 2,  # Piyoz
                "quantity": 0.2  # 200 gram
            }
        ])
    }
    
    response = requests.patch(
        f"{BASE_URL}/products/1/update/",  # Mahsulot ID=1
        data=data
    )
    print_response(response)

def test_ingredient_calculations():
    # Ma'lum sana uchun masalliqlar hisobi
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    print(f"\nErtangi ({tomorrow}) kun uchun masalliqlar hisobi:")
    
    response = requests.get(
        f"{BASE_URL}/ingredients/calculations/",
        params={'date': tomorrow.isoformat()}
    )
    print_response(response)

def print_response(response):
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")  # So'rov URL ini ham chiqaramiz
    try:
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Raw Response:", response.text)
    print("-" * 80)

if __name__ == "__main__":
    # 1. Mahsulot ingredientlarini qo'shish
    create_product_ingredients()
    
    # 2. Test buyurtma yaratish
    create_test_order()
    
    # 3. Hisoblarni tekshirish
    test_all_endpoints()

    # 4. Ertangi hisoblar
    test_ingredient_calculations()