from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.dashboard,name = 'dashboard'),
    path('add_product/',views.addProduct,name = 'add_product'),
    path('orders/',views.ordersListPage,name='orders'),
    path('view_order/<str:order_id>/',views.viewOrderDetails,name = 'view_order'),
    path('view_cart/<str:order_id>/',views.viewCartDetails,name = 'view_cart'),
    path('products_list/',views.productsList,name = 'products_list'),
    path('update_product/<str:product_id>/',views.updateProduct,name = 'update_product'),
    path('delete_product/<str:product_id>/',views.deleteProduct,name = 'delete_product'),
]
