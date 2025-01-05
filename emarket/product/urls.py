from django.urls import path
from . import views



urlpatterns = [
    path('products/', views.get_all_products, name='get_all_products'),
    path('products/new/', views.new_product, name='new_product'),  # Ensure this is not conflicting
    path('products/<int:id>/', views.get_by_id_product, name='get_by_id_product'),
    path('products/update/<int:pk>/', views.update_product, name='update-product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete-product'),
    # path('<str:pk>/reviews', views.create_review, name='create-review'),
    path('<int:pk>/reviews/', views.create_review, name='create-review'),
    path('<int:pk>/reviews/delete/', views.delete_review, name='delete-review'),



]
