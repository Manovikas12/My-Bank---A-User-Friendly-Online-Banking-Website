from django import forms

from accounts.models import User, Account

class DepositForm(forms.Form):
    amount = forms.DecimalField(label="Amount", min_value=0.01)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        # Check if the amount is valid
        if amount <= 0:
            raise forms.ValidationError("Invalid amount. Amount must be greater than 0.")

        return cleaned_data

class TransferForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    recipient = forms.CharField(label='Recipient account number')

    def clean_recipient(self):
        recipient_account_number = self.cleaned_data.get('recipient')
        try:
            recipient_account = Account.objects.get(account_number=recipient_account_number)
        except Account.DoesNotExist:
            raise forms.ValidationError('Recipient account does not exist')
        return recipient_account.account_number


from django import forms

class WithDrawForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')


        # Check if the amount is valid
        if amount <= 0:
            raise forms.ValidationError("Invalid amount. Amount must be greater than 0.")


        return cleaned_data

class LoanForm(forms.Form):
    # Personal Information
    full_name = forms.CharField(label='Full Name', max_length=100)
    date_of_birth = forms.DateField(label='Date of Birth')
    social_security_number = forms.CharField(label='Social Security Number', max_length=20)
    address = forms.CharField(label='Address', widget=forms.Textarea)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    email = forms.EmailField(label='Email Address')

    # Employment Information
    employer = forms.CharField(label='Current Employer', max_length=100)
    job_title = forms.CharField(label='Job Title', max_length=100)
    employment_status = forms.ChoiceField(label='Employment Status', choices=[('full_time', 'Full-time'), ('part_time', 'Part-time'), ('self_employed', 'Self-employed')])
    monthly_income = forms.DecimalField(label='Monthly Income', min_value=0, decimal_places=2)

    # Financial Information
    monthly_expenses = forms.DecimalField(label='Monthly Expenses', min_value=0, decimal_places=2)
    savings = forms.DecimalField(label='Savings', min_value=0, decimal_places=2)
    investments = forms.DecimalField(label='Investments', min_value=0, decimal_places=2)
    credit_score = forms.IntegerField(label='Credit Score')

    # Loan Details
    loan_amount = forms.DecimalField(label='Loan Amount Requested', min_value=0, decimal_places=2)
    loan_purpose = forms.CharField(label='Purpose of the Loan', max_length=100)
    loan_term = forms.IntegerField(label='Loan Term (in months)', min_value=1)
    repayment_schedule = forms.ChoiceField(label='Preferred Repayment Schedule', choices=[('monthly', 'Monthly'), ('biweekly', 'Bi-weekly')])

    # Collateral Information
    collateral_details = forms.CharField(label='Collateral Details', widget=forms.Textarea)

    # Co-signer Information
    has_cosigner = forms.BooleanField(label='Do you have a co-signer?', required=False)
    cosigner_full_name = forms.CharField(label='Co-signer Full Name', max_length=100, required=False)
    cosigner_social_security_number = forms.CharField(label='Co-signer Social Security Number', max_length=20, required=False)

    # Other Information
    additional_comments = forms.CharField(label='Additional Comments', widget=forms.Textarea, required=False)

    # Terms and Conditions
    agree_to_terms = forms.BooleanField(label='I agree to the Terms and Conditions', required=True)
