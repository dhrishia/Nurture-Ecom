
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views






urlpatterns = [
  
    path('dashboard',views.dashboardView, name="dashboard"),
    path('',views.AdminLoginView.as_view(), name="admin-login"),
    path('admin-logout',views.AdminLogoutView.as_view(), name="admin-logout"),
     
    path('products',views.productsView, name="admin-products"),
    path('users',views.usersView, name="admin-users"),
    path('add-product',views.addProductView, name="add-product"),
    path('save-product',views.saveProductView, name="save-product"),
    path('edit-product/<int:product_id>/',views.editProductView, name="edit-product"),
    path('delete-product/<int:product_id>/',views.deleteProductView, name="delete-product"),
    path('add-user',views.addUserView, name="add-user"),
    path('block-user/<int:user_id>/',views.user_action, name="block-user"),
    path('save-user',views.saveUserView, name="save-user"),
    path('edit-user/<int:user_id>/',views.editUserView, name="edit-user"),
    path('delete-user/<int:user_id>/',views.deleteUserView, name="delete-user"),
    path('categories',views.categoryView, name="admin-category"),
    path('add-category',views.addCategoryView, name="add-category"),
    path('save-category',views.saveCategoryView, name="save-category"),
    path('edit-category/<int:cat_id>/',views.editCategoryView, name="edit-category"),
    path('delete-category/<int:cat_id>/',views.deleteCategoryView, name="delete-category"),    
    path('viewcoupon/',views.view_coupons,name="viewcoupon"),
    path('addcoupon/',views.add_coupons,name="addcoupon"),
    path('editcoupon/<int:pid>/',views.edit_coupon,name="editcoupon"),
    path('deletecoupon/<int:pid>/',views.delete_coupon,name="deletecoupon"),
    path('orders/',views.manage_order,name="orders"),
    path('updateorder/<int:id>/',views.update_order,name='updateorder'),
    path('delete-image/<int:iid>/', views.delete_image, name='deleteimage'),






  

]




    