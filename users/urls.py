from django.urls import path
from users import views


urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('password-reset-success/', views.password_reset_success, name='password_reset_success'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  

    path('user/details/', views.user_details, name='user_details'),
    path('user/update/', views.user_update, name='user_update'),
    path('user/delete/', views.user_delete, name='user_delete'),

    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_details, name='post_details'),
    path('post/<slug:slug>/update/', views.update_post, name='update_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
]

