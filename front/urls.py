from django.urls import path

from front import views

app_name = 'front'

urlpatterns = [
    path('',views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/author/<str:redactor>/', views.post_author_details, name='post_author_details'),
    path('posts/category/<slug:slug>/', views.post_category_details, name='post_category_details'),
    path('posts/<slug:slug>/', views.post_details, name='post_details'),
    path('search_results/', views.search_results, name="search_results"),
    path('add_posts', views.add_posts, name='add_posts'),

    path('auth/login/', views.auth_log_in, name='auth_log_in'),
    path('auth/logout/', views.auth_sign_out, name='auth_sign_out'),
    path('auth/signin/', views.auth_sign_in, name='auth_sign_in'),

]
