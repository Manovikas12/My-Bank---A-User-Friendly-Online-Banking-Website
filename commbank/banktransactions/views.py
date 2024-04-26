from django.views import View
from django.shortcuts import render
from banktransactions.forms import DepositForm, WithDrawForm, TransferForm, LoanForm
from accounts.models import Account, Transaction, User
from django.shortcuts import redirect
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal


from django.db.models import F

class DepositMoneyView(View):
    template_name = 'banktransactions/depositmoney.html'

    def get(self, request):
        form = DepositForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            account = user.account  # Assuming each user has one account

            # Update account balance using F() object
            Account.objects.filter(user=user).update(balance=F('balance') + amount)

            # Create a deposit transaction
            Transaction.objects.create(user=user, amount=amount, transaction_type=Transaction.DEPOSIT)

            return render(request, self.template_name, {'form': form, 'success_message': f'Deposit of {amount} successful'})
        return render(request, self.template_name, {'form': form})

class WithdrawMoneyView(View):
    template_name = 'banktransactions/withdraw.html'

    def get(self, request):
        form = WithDrawForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = WithDrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            account = user.account  # Assuming each user has one account

            # Check if there's sufficient balance
            if account.balance < amount:
                return render(request, self.template_name, {'form': form, 'error_message': 'Insufficient balance'})

            # Update account balance using F() object
            Account.objects.filter(user=user).update(balance=F('balance') - amount)

            # Create a withdrawal transaction
            transaction = Transaction.objects.create(user=user, amount=amount, transaction_type=Transaction.WITHDRAW)

            return render(request, self.template_name, {'form': form, 'success_message': f'Withdrawal of {amount} successful'})
        return render(request, self.template_name, {'form': form})



from .forms import TransferForm  # Assuming you have a TransferForm defined in forms.py

from django.db import transaction
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import TransferForm
from django.db import transaction

class TransferMoneyView(View):
    template_name = 'banktransactions/transfermoney.html'

    def get(self, request):
        form = TransferForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_account_number = form.cleaned_data['recipient']
            user = request.user

            try:
                with transaction.atomic():
                    # Get sender's account
                    try:
                        sender_account = Account.objects.get(user=user)
                    except Account.DoesNotExist:
                        messages.error(request, 'Sender account not found')
                        return redirect(reverse('transfer_money'))

                    # Find recipient's account
                    try:
                        recipient_account = Account.objects.get(account_number=recipient_account_number)
                    except Account.DoesNotExist:
                        messages.error(request, 'Recipient account not found')
                        return redirect(reverse('transfer_money'))

                    # Check if sender has sufficient balance
                    if sender_account.balance < amount:
                        messages.error(request, 'Insufficient balance')
                        return redirect(reverse('transfer_money'))

                    # Deduct amount from sender's account
                    sender_account.balance -= amount
                    sender_account.save()

                    # Credit amount to recipient's account
                    recipient_account.balance += amount
                    recipient_account.save()

                    # Create transaction records
                    Transaction.objects.create(
                        user=user,
                        first_account_number=user.account.account_number,
                        #first_account_full_name=user.userinfo.first_name,
                        second_account_number=recipient_account_number,
                        #second_account_full_name=recipient_account_number.userinfo.first_name,
                        amount=amount,
                        transaction_type=Transaction.SENT
                    )

                    Transaction.objects.create(
                        user=recipient_account.user,
                        first_account_number=user.account.account_number,
                        #first_account_full_name= recipient_account_number.userinfo.first_name,
                        second_account_number=recipient_account_number,
                        #second_account_full_name= user.userinfo.first_name,
                        amount=amount,
                        transaction_type=Transaction.RECEIVED
                    )

                    messages.success(request, 'Transfer successful')
                return redirect(reverse('banktransactions:transfer_money'))
            except Exception as e:
                messages.error(request, 'Error processing transfer')
                print(e)
                print("Hello")
                return redirect(reverse('banktransactions:transfer_money'))
        else:
            messages.error(request, 'Invalid form data')
            return redirect(reverse('banktransactions:transfer_money'))


class TransactionReportView(View):
    template_name = 'banktransactions/transactionreport.html'

    def get(self, request):
        # Get the current user's account number
        user_account_number = request.user.account.account_number

        # Query transactions for the current user's account number and order them by date in descending order
        transactions = Transaction.objects.filter(user__account__account_number=user_account_number).order_by('-date')

        context = {'transactions': transactions}  # Create context with filtered transactions data
        return render(request, self.template_name, context)  # Render the template with filtered transactions


class LoanView(View):
    template_name = 'banktransactions/loans.html'


    def get(self, request):
        form = LoanForm()
        return render(request, self.template_name, {'form': form})


class PersonalLoanView(View):
    template_name = 'banktransactions/personalloan.html'

    def get(self, request):
        form = LoanForm()
        return render(request,self.template_name, {'form': form})

class HomeLoanView(View):
    template_name = 'banktransactions/homeloan.html'

    def get(self, request):
        form = LoanForm()
        return render(request, self.template_name, {'form': form})

class BusinessLoanView(View):
    template_name = 'banktransactions/businessloan.html'

    def get(self, request):
        form = LoanForm()
        return render(request, self.template_name, {'form': form})


import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def download_statement(request):
    # Retrieve transactions from the database
    all_transactions = Transaction.objects.all()

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Set up table headers
    headers = ["Amount", "Transaction Type", "First Account Number", "Second Account Number", "Date"]
    header_y = 750  # Initial y-coordinate for the headers
    for i, header in enumerate(headers):
        p.drawString(100 + i * 150, header_y, header)

    # Draw the transactions onto the PDF.
    y = 730  # Initial y-coordinate for the first transaction (below headers)
    for transaction in all_transactions:
        # Print Amount
        amount_text = str(transaction.amount) if transaction.amount is not None else "N/A"
        p.drawString(100, y, amount_text)

        # Print Transaction Type
        transaction_type_text = transaction.transaction_type if transaction.transaction_type is not None else "N/A"
        p.drawString(250, y, transaction_type_text)

        # Print First Account Number
        first_account_number_text = transaction.first_account_number if transaction.first_account_number is not None else "N/A"
        p.drawString(400, y, first_account_number_text)

        # Print Second Account Number
        second_account_number_text = transaction.second_account_number if transaction.second_account_number is not None else "N/A"
        p.drawString(550, y, second_account_number_text)

        # Print Date
        date_text = str(transaction.date) if transaction.date is not None else "N/A"
        p.drawString(650, y, date_text)

        y -= 20  # Adjust y-coordinate for the next transaction

    # Close the PDF object cleanly.
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="transaction_statement.pdf")
