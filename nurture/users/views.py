from django.shortcuts import render,redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import User
from products.models import *
from .form import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth import authenticate,login
import re






# Email Verification
from .token import *
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.core.mail import send_mail

# Forgot password
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


def home(request):
    return render(request, 'index.html')

class UserLoginView(LoginView): 
    template_name = 'login.html'
    authentication_form = UserLoginForm
    # form_class = UserLoginForm
    extra_context ={'title' : 'Login'}
    
    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data.get('username'))
        except(User.DoesNotExist):
            user = None
        if user and user.is_email_verified:
            return super().form_valid(form)
        else:
            form.add_error(None, error='User not verified')
            return super().form_invalid(form) 



class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = "register.html"
    extra_context = {'title': 'register'}
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the user object
        user = form.save(commit=False)

        # Send a verification email to the user
        form.instance.username = form.instance.email
        uid = urlsafe_base64_encode(force_bytes(user.email))

        token_generator = EmailVerificationTokenGenerator()
        token = token_generator.make_token(user)

        verification_link = f"{self.request.scheme}://{self.request.get_host()}{reverse_lazy('verify-email', kwargs={'uidb64': uid, 'token': token})}"
        send_mail(
            subject='Verify your email address',
            message=f'Please click the following link to verify your email address: {verification_link}',
            from_email='your@email.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)
    

class PasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    form_class = PasswordForgotForm
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetDoneView(generic.TemplateView):
    template_name = 'password_reset_form.html'
    extra_context = {'email': 'send'}

class PasswordResetCompleteView(generic.RedirectView):
    url = reverse_lazy('login') 

class EmailVerificationView(generic.TemplateView):
    template_name = 'login.html'
    extra_context ={'title' : 'Login'}
    
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(email=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            user.is_email_verified = True
            user.save()

            return redirect('login')
        else:
            return self.render_to_response({'success': False})
        

# @login_required(login_url='/login')
# def profile(request):
#     context = {
#         'user_addresses': Address.objects.filter(customer=request.user).order_by('id')
#      }
#     return render(request, 'users/profile.html',context)

@never_cache
@login_required(login_url='login')
def profile(request):
    if request.user.is_authenticated:
        return render(request,'users/profile.html')
    else:
        return redirect('login')
    

@never_cache
@login_required(login_url='login')
def addressView(request):
    addresses = Address.objects.filter(customer=request.user)
    if request.method == 'POST':
        selected_addresses = request.POST.getlist('selected_addresses')
        if selected_addresses is None:
            messages.success(request,"Select an Address")
        else:
            Address.objects.filter(id__in=selected_addresses).delete()
            messages.success(request, "Address Deleted")
            return redirect(addressView)
    
    
    return render(request, 'users/address.html', {'addresses': addresses})




 


@never_cache
@login_required(login_url='login')
def add_address(request,id):
    id=id
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    if request.method == 'POST':
        address = Address(
            customer=request.user,
             address_line_1=request.POST['address_line_1'],
            address_line_2=request.POST.get('address_line_2', ''),
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
        )
        address.save()
        if request.POST.get('default', '') == 'on':
            Address.objects.filter(customer=request.user).exclude(id=address.id).update(default=False)
            address.default=True
            address.save()

        if id==0 :
            return redirect('profile')
        else :
            return redirect('checkout')
    else:
        context = {
            'state': state,
            'city': city,
        }
    return render(request, 'users/addaddress.html',context)

@never_cache
@login_required(login_url='login')
def edit_address(request, address_id):
    state = ['Kerala', 'AndraPradesh', 'Karnataka', 'Tamilnadu']
    city = ['Kannur','Kozhikkode','Ernakulam','Thiruvananthapuram','Banglore','Hubli','Hydrabad','Coimbator','Madurai']
    newaddress = Address.objects.get(id= address_id)
    if request.method == 'POST':
        newaddress.address_line_1=request.POST['address_line_1']
        newaddress.address_line_2=request.POST.get('address_line_2', '')
        newaddress.city=request.POST['city']
        newaddress.state=request.POST['state']
        newaddress.pincode=request.POST['pincode']
        newaddress.save()
        if request.POST.get('default', '') == 'on':
            Address.objects.filter(customer=request.user).exclude(id=newaddress.id).update(default=False)
            newaddress.default=True
            newaddress.save()
        messages.success(request,"Your Address successfully edited")
        return redirect(addressView)
    
    context = {
        'state': state,
        'city' : city,
        'newaddress' : newaddress
    }

    return render(request, 'users/editaddress.html',context)




@never_cache
@login_required(login_url='login')
def updateprofile(request):
    user_form = UserForm(instance=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user = user_form.save()
            if 'image' in request.FILES:
                user.image = request.FILES['image']
                user.save()
            messages.info(request, 'Updated Successfully')
            return redirect('profile')

    return render(request, 'users/updateuserprofile.html', {
        'user_form': user_form,
    })



@never_cache
@login_required(login_url='login')
def changepassword(request):
    if request.method == 'POST':
        oldpass = request.POST['currentpassword']
        newpass = request.POST['newpassword']
        confirm_newpass = request.POST['confirmpassword']
        user = authenticate(username=request.user.username, password=oldpass)
        if user:
            if oldpass == newpass:
                messages.error(request, "New Password should not be the Previous Password")
                return redirect(changepassword)
            elif newpass != confirm_newpass:
                messages.error(request, "Password not matching")
                return redirect(changepassword)
            elif not re.match(r'^(?=.*[A-Z])[A-Za-z\d]{6,}$', newpass):
                messages.error(request, "Password must be at least 6 characters long and contain at least one uppercase letter")
                return redirect(changepassword)
            else:
                user.set_password(newpass)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('login')
        else:
            messages.error(request, "Invalid Password")
            return redirect(changepassword)
    return render(request, 'users/changepassword.html')


@never_cache
@login_required(login_url='login')
def orderHistoryView(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'users/orderhistory.html', {'orders': orders})
@never_cache
@login_required(login_url='login')
def viewOrder(request, id):
    order =Order.objects.filter(id=id,user=request.user).first()
    orderitems = OrderProduct.objects.filter(order=order)

    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'users/orderview.html',context)
        