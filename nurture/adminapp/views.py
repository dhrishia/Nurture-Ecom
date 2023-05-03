from django.shortcuts import render,HttpResponseRedirect

# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from users.models import *
from products.models import *
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control
from products.forms import CouponForm
from django.conf import settings
import os






from django.contrib.auth.decorators import user_passes_test

def super_user_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url='admin-login')(view_func)
    
    return decorated_view_func

class AdminLoginView(LoginView): 
    template_name = 'login.html'
    extra_context ={'title' : 'Login-admin'}
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        return self.success_url
    
    
class AdminLogoutView(LogoutView):
    next_page = '/adminapp/'


def dashboardView(request):
    # products = Product.objects.all()

    # context = {'products': products}
    return render(request, 'admin/dashboard.html')

def productsView(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'admin/products.html',context)

def addProductView(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'admin/addproduct.html', context)
   


def saveProductView(request):
    if request.method == 'POST':
        name=request.POST['name']
        category=request.POST['category']
        #here only the id of category will be stored
 
        stock=request.POST['stock']
        price=request.POST['price']
        images = request.FILES.getlist('image')
        

        if not name:
            messages.warning(request, 'Product name should not be empty')
            return redirect('add-product')
        
        if not all(char.isalpha() or char.isspace() for char in name) or len(name.strip()) == 0:
            messages.warning(request, 'Invalid entry for product name')
            return redirect('add-product')
        
        if Product.objects.filter(name=name).exists():
            messages.info(request,"This product already exists")
            return redirect('add-product')
       

        
        
        if not stock.isdigit():
            messages.warning(request,'Invalid entry for stock')
            return redirect('add-product')
                
        if not str(price).isnumeric() and 'e' not in price.lower():
            try:
                float(price)
                if float(price) < 0:
                    messages.warning(request, 'Price cannot be negative')
                    return redirect('add-product')

            except ValueError:
                messages.warning(request, 'Invalid entry for price')
                return redirect('add-product')


        if 'e' in price.lower() or float(price) > 1000000:
            messages.warning(request,'Enter only numbers, scientific notation not allowed, and the price should not exceed 1000000')
            return redirect('add-product')
        
        
    
        cat_instance = Category.objects.get(id=category)
        

        prod = Product.objects.create(
            name=name,
            category=cat_instance,
            stock=stock,
            price=price,
          )
        prod.save()
        
        for image in images:
            ProductImage.objects.create(product=prod, images=image)
        return redirect('admin-products')
        
         
    else:
        return redirect('add_product')
    

def editProductView(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    images = ProductImage.objects.filter(product=product)

    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        image = request.FILES['image']
        print(image, "=====================")
        stock = request.POST['stock']
        catobj = Category.objects.get(id=cat)
        if int(price) < 0:
            messages.warning(request,"Enter a valid quantity")
            return redirect('edit-product',product_id)
        else:
             # Update product attributes
            Product.objects.filter(id=product_id).update(name=name, price=price, category=catobj ,stock=stock, image=image)

             # Get the new images uploaded during editing
            new_images = request.FILES.getlist('images')
            for image in new_images:
                ProductImage.objects.create(product=product, images=image)
       
            messages.success(request, "Product Updated")
            return redirect('admin-products')
    return render(request, 'admin/editproduct.html', locals())


@user_passes_test(lambda u:u.is_superuser,login_url='adminlogin')
def delete_image(request, iid):
    image = ProductImage.objects.get(id=iid)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image.images))
    os.remove(image_path)
    product_id = image.product.id if image.product else None
    image.delete()
    if product_id:
        return HttpResponseRedirect(reverse(editProductView, args=[product_id]))
    else:
        return HttpResponseRedirect(reverse(productsView))
    


def deleteProductView(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    del_record = Product.objects.filter(id=product_id)
    del_record.delete()
    messages.success(request, f"{product.name} has been deleted from the list")    
    return redirect('admin-products')





# users management--------------------------------


def addUserView(request):
 
     return render(request, 'admin/adduser.html')



def saveUserView(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
         #here only the id of category will be stored
 
        email=request.POST['email']
         
        

        if not first_name:
            messages.warning(request, 'Product name should not be empty')
            return redirect('add-product')
        
        if not all(char.isalpha() or char.isspace() for char in first_name) or len(first_name.strip()) == 0:
            messages.warning(request, 'Invalid entry for user first name')
            return redirect('add-user')
        
        if User.objects.filter(email=email).exists():
            messages.info(request,"This user already exists")
            return redirect('add-user')
       

         
        user_data = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email
         )
        user_data.save()
        return redirect('admin-users')
         

    else:
        return redirect('add_user')



def usersView(request):
    users = User.objects.all()

    context = {'users': users}
    return render(request, 'admin/users.html',context)




def editUserView(request, user_id):
    users_datas = User.objects.get(id=user_id)
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
  
        User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name, email=email)

             # Get the new images uploaded during editing
        messages.success(request, "User data Updated")
        return redirect('admin-users')
    return render(request, 'admin/adduser.html', locals())


def deleteUserView(request,user_id):
    user = get_object_or_404(User,id=user_id)
    del_record = User.objects.filter(id=user_id)
    del_record.delete()
    messages.success(request, f"{user.first_name} has been deleted from the list")    
    return redirect('admin-users')


@super_user_required
def user_action(request, user_id): 
    try:
        user = User.objects.get(id=user_id)
    except:
        user = None

    if user.is_blocked == False:
        user.is_blocked = True
        user.save()
    else:
        user.is_blocked = False
        user.save()

    return redirect('admin-users')

    



# category management--------------------------------


def addCategoryView(request):
 
     return render(request, 'admin/addcategory.html')



def saveCategoryView(request):
    if request.method == 'POST':
        name=request.POST['name']
        slug=request.POST['slug']
  
          
        

        if not name:
            messages.warning(request, 'category name should not be empty')
            return redirect('add-category')
        
        if not all(char.isalpha() or char.isspace() for char in name) or len(name.strip()) == 0:
            messages.warning(request, 'Invalid entry for user category name')
            return redirect('add-category')
        
        if Category.objects.filter(name=name).exists():
            messages.info(request,"This Category already exists")
            return redirect('add-category')
       

         
        cat_data = Category.objects.create(
            name=name,
            slug = slug
            )
             
        cat_data.save()
        return redirect('admin-category')
         

    else:
        return redirect('add_category')



def categoryView(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'admin/categories.html',context)




def editCategoryView(request, cat_id):
    category = Category.objects.get(id=cat_id)
    if request.method == "POST":
        name = request.POST['name']
        slug = request.POST['slug']
  
  
        Category.objects.filter(id=cat_id).update(name=name, slug=slug)

             # Get the new images uploaded during editing
        messages.success(request, "category Updated")
        return redirect('admin-category')
    return render(request, 'admin/addcategory.html', locals())


def deleteCategoryView(request,cat_id):
    category = get_object_or_404(Category,id=cat_id)
    del_record = Category.objects.filter(id=cat_id)
    del_record.delete()
    messages.success(request, f"{category.name} has been deleted from the list")    
    return redirect('admin-category')

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def view_coupons(request):
    coupons = Coupon.objects.all()
    return render(request,'admin/coupon.html',{'coupons':coupons})

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(view_coupons)
    else:
        form = CouponForm()
    return render(request, 'admin/addcoupon.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def edit_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)

    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Updated")
            return redirect(view_coupons)
    else:
        form = CouponForm(instance=coupon)

    return render(request, 'admin/editcoupon.html', {'form': form, 'coupon': coupon})


@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)
    coupon.delete()
    messages.success(request, "Coupon Deleted")
    return redirect(view_coupons)
    

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def manage_order(request):
    orders=Order.objects.all().order_by('created_at')
    return render(request, 'admin/orders.html', locals())

@user_passes_test(lambda u: u.is_superuser)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def update_order(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        status = request.POST.get('status')
        if(status):
            order.status = status
            order.save()
        if status  == "Delivered":
            try:
                payment = Payment.objects.get(payment_id = order.order_number, status = False)
                if payment.payment_method == 'Cash on Delivery':
                    payment.paid = True
                    payment.save()
            except:
                pass
    return redirect(manage_order)



