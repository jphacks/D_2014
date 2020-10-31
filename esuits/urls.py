from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('escreate/', views.ESCreateView.as_view(), name='es_create')
]
