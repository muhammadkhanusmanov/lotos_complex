from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def profile_view(request):
    user = request.user
    return JsonResponse({
        'user_id': user.user_id,
        'first_name': user.first_name,
        'phone_number': user.phone_number
    })

@csrf_exempt
def telegram_auth(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            first_name = data.get('first_name')
            last_name = data.get('last_name', '')
            phone_number = data.get('phone_number', '')
            
            if not user_id or not first_name:
                return JsonResponse({'error': 'user_id and first_name are required'}, status=400)
            
            user, created = TelegramUser.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number
                }
            )
            
            if not created:
                # Yangilanish kerak bo'lsa
                user.first_name = first_name
                user.last_name = last_name
                if phone_number:
                    user.phone_number = phone_number
                user.save()
            
            return JsonResponse({
                'status': 'success',
                'user_id': user.user_id,
                'first_name': user.first_name
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)