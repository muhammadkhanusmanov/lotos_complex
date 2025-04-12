import requests
import json
from datetime import datetime, timedelta
import os

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    # 1. Mahsulotlar ro'yxatini olish
    print("\n1. Mahsulotlar ro'yxati:")
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response)
    
    # Birinchi mahsulot ID sini saqlab olamiz
    products = response.json()
    if products:
        product_id = products[0]['id']
        
        # 2. Bitta mahsulot ma'lumotlarini olish
        print("\n2. Mahsulot ma'lumotlari:")
        response = requests.get(f"{BASE_URL}/products/{product_id}/")
        print_response(response)
        
        # 3. Yangi buyurtma yaratish
        print("\n3. Yangi buyurtma yaratish:")
        order_data = {
            "telegram_user_id": 123456789,
            "customer_name": "Test User",
            "phone_number": "+998901234567",
            "items": [
                {
                    "product": product_id,
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
        
        # Buyurtma ID sini saqlab olamiz
        if response.status_code == 201:
            order_id = response.json()['id']
            
            # 4. Buyurtma ma'lumotlarini olish
            print("\n4. Buyurtma ma'lumotlari:")
            response = requests.get(f"{BASE_URL}/orders/{order_id}/")
            print_response(response)
    
    # 5. Bugungi masalliqlar hisobi
    print("\n5. Bugungi masalliqlar hisobi:")
    response = requests.get(f"{BASE_URL}/ingredients/calculations/")
    print_response(response)
    
    # 6. Haftalik masalliqlar hisobi
    print("\n6. Haftalik masalliqlar hisobi:")
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    response = requests.get(
        f"{BASE_URL}/ingredients/calculations/daily/",
        params={
            'start_date': week_ago.isoformat(),
            'end_date': today.isoformat()
        }
    )
    print_response(response)
    
    

def print_response(response):
    print(f"Status: {response.status_code}")
    print("Headers:", dict(response.headers))
    try:
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Raw Response:", response.text)
    print("-" * 80)

if __name__ == "__main__":
    test_endpoints()  # Mavjud testlar
    test_create_endpoints()  # Yangi testlar