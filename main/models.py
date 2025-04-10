from django.db import models

class TelegramUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True, unique=True)  # telegram_id
    first_name = models.CharField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} ({self.user_id})"