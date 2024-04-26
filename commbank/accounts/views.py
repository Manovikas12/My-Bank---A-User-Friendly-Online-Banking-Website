from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import get_user_model, login, logout
from .forms import LoginForm
from django.views import View
# Create your views here.


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    template_name = 'mainsystem/index.html'  # Specify the HTML file

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)

        return render(request, self.template_name)


def profile(request):
    pass

def bank_statement(request):
    pass

def transfer_money(request):
    pass

def homeloan(request):
    pass

def insurance(request):
    pass

def business(request):
    pass

def investing(request):
    pass

def banking(request):
    pass


def help(request):
    pass

def financial_assistance(request):
    pass

def complaints(request):
    pass

def payment_services(request):
    pass

def about_us(request):
    pass

def careers(request):
    pass

def sustainability(request):
    pass

def newsroom(request):
    pass

def investor_centre(request):
    pass

def facebook(request):
    pass

def linkedin(request):
    pass

def youtube(request):
    pass

def instagram(request):
    pass

def security(request):
    pass


