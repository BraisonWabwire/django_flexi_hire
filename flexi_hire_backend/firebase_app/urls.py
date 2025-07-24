from django.urls import path
from firebase_app import views 

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('job/delete/<str:job_id>/', views.delete_job_view, name='delete_job'),
    path('job/edit/<str:job_id>/', views.edit_job_view, name='edit_job'),
]
