from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing, name='landing'),
    path('About', views.about, name='about'),
    path('Sign_in', views.Sign_in, name='Sign_in'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('For_enterprises', views.For_enterprises, name='For_enterprises'),
    path('enterprise-register', views.Enterprise_register, name='Enterprise_register'),
    path('enterprise-login', views.Enterprise_login, name='Enterprise_login'),
    path('enterprise-admin', views.Enterprise_admin, name='Enterprise_admin'),
    path('user-dashboard', views.user_dashboard, name='user_dashboard'),
    path('user-dashboard-order-history', views.user_dashboard_order_history, name='user_dashboard_order_history'),
    path('user-db-profile', views.user_db_profile, name='user_db_profile'),
    path('user-dashboard-menu/', views.user_dashboard_menu, name='user_dashboard_menu'),
    path('supplier-dashboard', views.supplier_dashboard, name='supplier_dashboard'),
    path('supplier-dashboard-menu', views.supplier_dashboard_menu, name='supplier_dashboard_menu'),
    path('supplier-db-profile', views.supplier_db_profile, name='supplier_db_profile'),
    path('supplier-dashboard-order-history', views.supplier_dashboard_order_history, name='supplier_dashboard_order_history'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.view_cart, name='view_cart'),
    path('place_order', views.place_order, name='place_order'),
    path('update_cart/<str:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('accept-order/<str:order_id>/', views.accept_order, name='accept_order'),
    path('reject-order/<str:order_id>/', views.reject_order, name='reject_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)