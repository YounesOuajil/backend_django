from django.urls import path
from .views import login,signup,email_verified,reset_password,reseted_password

urlpatterns = [
    path('login/',view=login),
    path('signup/',view=signup),
    path('email_verified/<str:uidb64>/<str:token>/',view=email_verified),
    path('reset_password/',view=reset_password),
    path('reseted_password/<str:uidb64>/<str:token>/',view=reseted_password),

]
