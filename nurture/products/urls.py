
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views






urlpatterns = [
  
    path('plants/<int:id>/',views.plantsView, name="plants"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('product-detail/<int:pk>/', views.detailView, name="product-detail"),
    path('add-to-wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/', views.cartView, name='cart'),
    path('cart-remove/<int:cart_id>/', views.cartDeleteView, name='cart-remove'),
    path('add-item-cart/<int:cart_id>/', views.add_item_cart, name='add-item-cart'),
    path('remove-item-cart/<int:cart_id>/', views.remove_item_cart, name='remove-item-cart'),
    path('removewishlist/<int:item_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('checkout/',views.checkout, name='checkout'),
    path('confirmation/',views.confirmation, name='confirmation'),
    path('order-complete/<str:ordernumber>/',views.orderComplete, name='order_complete'),
    path('place_order/', views.placeOrder, name='place_order'),
    path('cancel-order/<int:id>/',views.cancelOrder, name='cancel_order'),
    path('wishlist/', views.wishlistView, name='wishlist'),
    path('search/', views.search, name='search'),
    path('proceed_to_pay/',views.razorPayCheck,name="razorpaycheck"),

    


]




    