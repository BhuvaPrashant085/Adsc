from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('create/', views.create_issue, name='create_issue'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('filter_search/', views.filter_search, name='filter_search'),

    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]
