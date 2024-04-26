from django.urls import path
from .views import (
    UserLoginView, LogoutView, profile, bank_statement,
    transfer_money, banking, homeloan, insurance, business,
    investing, security, help, financial_assistance, complaints,
    payment_services, about_us, careers, sustainability, newsroom,
    investor_centre, facebook, linkedin, youtube, instagram,complaints,
    payment_services,
    about_us,
    careers,
    sustainability,
    newsroom,
    investor_centre,
)

app_name = 'accounts'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path('profile/', profile, name='profile'),
    path('bank_statement/', bank_statement, name='bank_statement'),
   # path('transfer_money/', transfer_money, name='transfer_money'),
    path('banking/', banking, name='banking'),
    path('homeloan/', homeloan, name='homeloan'),
    path('insurance/', insurance, name='insurance'),
    path('business/', business, name='business'),
    path('investing/', investing, name='investing'),
    path('facebook/', facebook, name='facebook'),
    path('linkedin/', linkedin, name='linkedin'),
    path('youtube/', youtube, name='youtube'),
    path('instagram/', instagram, name='instagram'),
    path('security/',security,name='security'),
    path('help/',help,name='help'),
    path('financial_assistance',financial_assistance, name='financial_assistance'),
    path('complaints/', complaints, name='complaints'),
    path('payment_services/', payment_services, name='payment_services'),
    path('about_us/', about_us, name='about_us'),
    path('careers/', careers, name='careers'),
    path('sustainability/', sustainability, name='sustainability'),
    path('newsroom/', newsroom, name='newsroom'),
    path('investor_centre/', investor_centre, name='investor_centre'),
]
