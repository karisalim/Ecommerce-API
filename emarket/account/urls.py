from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('userinfo/', views.current_user, name='userinfo'),
    path('userinfo/update/', views.update_user, name='update-user'),
    # path('forgot_password/update/', views.forgot_password, name='forgot-password'),
    path('forgot_password/', views.forgot_password, name='forgot-password'),  # Changed here
    # path('reset_password<str:token>/', views.reset_password, name='reset-password'),  # Changed here
    path('reset_password/<str:token>/', views.reset_password, name='reset-password'),  # Added slash here

]
