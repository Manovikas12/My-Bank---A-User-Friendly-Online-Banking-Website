from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import UserManager

class User(AbstractUser):
    username = None
    client_id = models.IntegerField(unique=True, primary_key=True, null=False, blank=False)
    objects = UserManager()
    USERNAME_FIELD = 'client_id'
    REQUIRED_FIELDS = []
    def __str__(self):
        return str(self.client_id)

class BranchInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    BSB_number = models.CharField(max_length=6, unique=True)
    branch_city = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=255)
    branch_address = models.CharField(max_length=512)
    branch_manager = models.CharField(max_length=255)
    branch_phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Branch - {self.BSB_number} ({self.branch_city})"

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.first_name

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(primary_key=True, unique=True, default='1000', max_length=20)  # Example max_length value
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Account - {self.account_number}"


import uuid

class Transaction(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'

    TRANSACTION_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdrawal'),
        (SENT, 'Sent'),
        (RECEIVED, 'Received'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    first_account_number = models.CharField(max_length=20, blank=True, null=True)
    first_account_full_name = models.CharField(max_length=20, blank=True, null=True)
    second_account_number = models.CharField(max_length=20, blank=True, null=True)
    second_account_full_name = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.transaction_type == self.SENT:
            try:
                account = Account.objects.get(account_number=self.second_account_number)
                user_info = UserInfo.objects.get(user=account.user)
                return f"Sent {self.amount} to {user_info.first_name} {user_info.last_name} on {self.date}"
            except Account.DoesNotExist:
                return f"Sent {self.amount} to unknown recipient on {self.date}"
            except UserInfo.DoesNotExist:
                return f"Sent {self.amount} to unknown recipient on {self.date}"
        elif self.transaction_type == self.RECEIVED:
            try:
                account = Account.objects.get(account_number=self.second_account_number)
                user_info = UserInfo.objects.get(user=account.user)
                return f"Received {self.amount} from {user_info.first_name} {user_info.last_name} on {self.date}"
            except Account.DoesNotExist:
                return f"Received {self.amount} from unknown sender on {self.date}"
            except UserInfo.DoesNotExist:
                return f"Received {self.amount} from unknown user on {self.date}"
        elif self.transaction_type == self.DEPOSIT:
            return f"Deposited {self.amount} on {self.date}"
        elif self.transaction_type == self.WITHDRAW:
            return f"Withdrew {self.amount} on {self.date}"
        else:
            return f"Unknown transaction type ({self.transaction_type}) for {self.amount} on {self.date}"

