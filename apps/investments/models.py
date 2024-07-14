from django.db import models

from apps.clients.models import InvestorProfile
from apps.commons.models import BaseModel


# Create your models here.
class InvestorCurrency(BaseModel):
    class Meta:
        unique_together = [["investor", "currency"]]

    currency = models.CharField(max_length=3)
    investor = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE)
    mean_value = models.DecimalField(decimal_places=10, max_digits=50)
    quantity = models.BigIntegerField()


class InvestorTradeCurrency(BaseModel):
    currency = models.CharField(max_length=3)
    investor = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE)
    unit_value = models.DecimalField(decimal_places=10, max_digits=50)
    quantity = models.BigIntegerField()
