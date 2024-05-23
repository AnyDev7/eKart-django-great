from django.urls import path
from ecart import views

urlpatterns = [
    path('', views.ecart, name="ecart"),
    path('add-prod/<int:product_id>/<int:flag>/', views.add_prod, name="add_prod"),
    path('remove-item/<int:product_id>/<int:cart_item_id>/', views.remove_item, name="remove_item"),
    path('minus-add-to-prod/<int:product_id>/<int:cart_item_id>/<int:flag>/', views.minus_add_to_prod, name="minus_add_to_prod"),
]

