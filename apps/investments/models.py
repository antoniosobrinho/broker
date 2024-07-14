from django.db import models

from apps.clients.models import InvestorProfile


# Create your models here.
class InvestorCurrency(models.Model):
    currency = models.CharField(max_length=3)
    investor = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE)
    mean_value = models.DecimalField(decimal_places=10, max_digits=50)
