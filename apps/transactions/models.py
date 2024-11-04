from django.db import models
from django.conf import settings

class Transaction(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='client_transaction')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='agent_transaction')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=[("deposit", "Deposit"), ("withdrawal", "Withdrawal")])
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True,null=True)


    def __str__(self):
        return f' Transaction {self.id} - {self.transaction_type} of {self.amount} by {self.client.username}'