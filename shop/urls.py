from django.urls import path
from . import views

urlpatterns = [
    # Frontend Page
    path('', views.index_view, name='index'),
    
    # Auth Endpoints
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
    path('api/auth/status/', views.api_auth_status, name='api_auth_status'),
    
    # Configuration / Settings Endpoints
    path('api/settings/', views.api_settings, name='api_settings'),
    
    # Product CRUD Endpoints
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/<uuid:pk>/', views.api_product_detail, name='api_product_detail'),
    
    # Reviews Endpoints
    path('api/reviews/', views.api_reviews, name='api_reviews'),
    
    # Orders Endpoints
    path('api/orders/', views.api_orders, name='api_orders'),
]
