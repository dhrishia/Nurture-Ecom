
from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from .form import *
from . import views



urlpatterns = [
        path('', home, name='home'),
        path('register/', UserRegisterView.as_view(), name='register'),
        path('login/', UserLoginView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),        
        path('password_reset/', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
        path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_form.html'), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class = PasswordSetForm), name='password_reset_confirm'),
        path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),  
        path('verify-email/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(template_name = 'login.html'), name='verify-email'),  
        path('profile/', views.profile, name="profile"), 
        path('useraddress/',addressView, name='useraddress'),
        path('addaddress/<int:id>',add_address, name='addaddress'),
        path('edit-address/<int:address_id>/',edit_address, name='edit_address'),
        path('updateprofile',updateprofile,name="updateuserprofile"),
        path('changepassword/',changepassword,name="changepassword"),
        path('orderhistory/', orderHistoryView, name='orderhistory'),
        path('vieworder/<int:id>/',viewOrder, name='vieworder'),



 

 

        ]
