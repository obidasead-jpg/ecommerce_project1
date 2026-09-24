from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # حسابات
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # السلة
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # إدارات المطور
    path('developer/add-product/', views.developer_add_product, name='developer_add_product'),
    path('developer/edit-product/<int:pk>/', views.developer_edit_product, name='developer_edit_product'),
    path('developer/delete-product/<int:pk>/', views.developer_delete_product, name='developer_delete_product'),
    
    # AI
    path('ai-chat/', views.ai_chatbot, name='ai_chatbot'),
]