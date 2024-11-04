from django.db import models
from django.conf import settings
from apps.transactions.models import Transaction


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name= 'user_notification')
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name='transaction_notification')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=[
            ("transaction_alert", "Transaction Alert"), 
            ("payment_reminder", "Payment Reminder")
        ])

    def __str__(self):
        return f'Notification {self.id} for {self.user.username} - {self.notification_type}'