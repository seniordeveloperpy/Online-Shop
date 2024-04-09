from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    
    path('', views.index, name='index'),

    # ------CATEGORY------------
    path('category-list', views.category_list, name='category_list'),
    path('category-create', views.category_create, name='category_create'),
    path('category-update/<str:code>/', views.category_update, name='category_update'),
    path('category-delete/<str:code>/', views.category_delete, name='category_delete'),

    # ------PRODUCT------------
    path('product-list', views.product_list, name='product_list'),
    path('product-create', views.product_create, name='product_create'),
    path('product-detail/<str:code>/', views.product_detail, name='product_detail'),
    path('product-update/<str:code>/', views.product_update, name='product_update'),
    path('product-delete/<str:code>/', views.product_delete, name='product_delete'),

    # ------PRODUCT IMG------------
    path('product-img-delete/<int:id>/', views.product_img_delete,name='product_img_delete'),
    path('product-video-delete/<int:id>/', views.product_video_delete,name='product_video_delete'),

    #-------ENTER-PRODUCT------------
    path('create-enter-product/', views.create_enter_product, name='create_enter_product'),
    path('list-enter-product/<str:code>/', views.list_enter_product, name='list_enter_product'),
    path('enter-product-history/<str:code>/', views.product_history, name='product_history'),
    path('update-enter-product/<str:code>/', views.update_enter_product, name='update_enter_product'),

    

]