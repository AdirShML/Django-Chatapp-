from django.urls import path
from . import views

urlpatterns = [
   path('', views.main_page, name='main'),
   path('login/', views.login_page, name='login'),
   path('signup/', views.signup_page, name='signup'),
   path('logout/', views.logout_user, name='logout'),
   path('<str:room_name>/', views.room_view, name='room'),
]