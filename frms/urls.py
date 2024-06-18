"""
URL configuration for frms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    CompanyCreateView,
    BranchCreateView,
    AdminUserCreateView,
    FinanceCashierUserCreateView,
    UserLoginView,
    UserTreeView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProductPriceHistoryListCreateView,
    BranchStockListCreateView,
    BranchStockRetrieveUpdateDestroyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', CompanyCreateView.as_view(), name='company-create'),
    path('branches/', BranchCreateView.as_view(), name='branch-create'),
    path('admin-users/', AdminUserCreateView.as_view(), name='admin-user-create'),
    path('user-tree/', UserTreeView.as_view(), name='user-tree'),
    path('finance-cashier-users/', FinanceCashierUserCreateView.as_view(), name='finance-cashier-user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('product-price-history/', ProductPriceHistoryListCreateView.as_view(), name='product-price-history-list-create'),
    path('branch-stocks/', BranchStockListCreateView.as_view(), name='branch-stock-list-create'),
    path('branch-stocks/<int:pk>/', BranchStockRetrieveUpdateDestroyView.as_view(), name='branch-stock-retrieve-update-destroy'),
    # Add other routes as needed
]
