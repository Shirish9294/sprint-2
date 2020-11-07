from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list, name='p_list'),
    path('<slug:category_slug>/', views.product_list,
         name='p_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='p_detail'),
]
