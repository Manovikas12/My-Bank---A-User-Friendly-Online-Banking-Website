from django.urls import path

from .views import DepositMoneyView, WithdrawMoneyView, TransferMoneyView, TransactionReportView, LoanView, PersonalLoanView, HomeLoanView, BusinessLoanView, download_statement


app_name = 'banktransactions'



urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),

    path('transfer/',TransferMoneyView.as_view(), name="transfer_money"),

    path('report/', TransactionReportView.as_view(), name="transaction_report"),
    path('loans/', LoanView.as_view(), name="loans"),
    path('personalloan/', PersonalLoanView.as_view(), name='personal_loan'),
    path('homeloan/', HomeLoanView.as_view(), name='home_loan'),
    path('businessloan/', BusinessLoanView.as_view(), name='business_loan'),

    path('download/', download_statement, name='download_statement'),


]
