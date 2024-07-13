from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.commons.models import Bank, BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)


class InvestorProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    address = models.TextField()
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=500)


class InvestorBankAccount(BaseModel):
    class Meta:
        unique_together = [["bank", "account_number"]]

    investor = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    account_number = models.PositiveIntegerField()

    def __str__(self):
        return self.investor.user.username + self.bank.name


class BankTransition(BaseModel):
    amount = models.DecimalField(decimal_places=2, max_digits=500)
    bank_account = models.ForeignKey(InvestorBankAccount, on_delete=models.PROTECT)
