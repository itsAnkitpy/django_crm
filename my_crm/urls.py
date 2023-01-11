from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Profiles and other pages
    path('user/',views.userPage,name='user_page'),
    path('account/',views.accountSettings,name='account'),

    path('',views.home,name='home'),
    path('customer/<str:pk>/',views.customer,name='customer'),
    path('product/',views.products,name='product'),
    path('orders/',views.order,name='orders'),
    
    # CRUD Paths
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),

    # Django authentication paths
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='my_crm/password_reset.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='my_crm/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='my_crm/password_reset_form.html'),name='password_reset_confirm'), 
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='my_crm/password_reset_done.html'),name='password_reset_complete'),
]
