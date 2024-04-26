from django.views.generic import TemplateView
from accounts.models import Account, Transaction
import os
from django.db.models import Sum
import io
from django.http import FileResponse
import matplotlib.pyplot as plt

from django.utils import timezone
from datetime import timedelta

from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta

class HomeView(TemplateView):
    template_name = 'mainsystem/userpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Retrieve the last ten transactions for the current user
            last_ten_transactions = Transaction.objects.filter(user=self.request.user).order_by('-id')[:4]
            context['last_ten_transactions'] = last_ten_transactions
        except Transaction.DoesNotExist:
            # Handle the case where no transactions are found
            context['last_ten_transactions'] = None
            # Log the error or provide a fallback behavior

        # Calculate the date 30 days ago
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # Retrieve all transactions within the last 30 days
        recent_transactions = Transaction.objects.filter(date__gte=thirty_days_ago)

        # Define variables to hold ongoing_amount and incoming_amount
        ongoing_amount = 0
        incoming_amount = 0

        # Loop through each transaction in the recent transactions list
        for transaction in recent_transactions:
            # Check the transaction type and update the corresponding amount variable
            if transaction.transaction_type == 'SENT' or transaction.transaction_type == 'WITHDRAW':
                ongoing_amount += transaction.amount
            elif transaction.transaction_type == 'RECEIVED' or transaction.transaction_type == 'DEPOSIT':
                incoming_amount += transaction.amount

        # Add the calculated amounts and recent transactions to the context
        context['recent_transactions'] = recent_transactions
        context['ongoing_amount'] = ongoing_amount
        context['incoming_amount'] = incoming_amount

        return context




class MainBankPageView(TemplateView):
    template_name = 'mainsystem/index.html'

