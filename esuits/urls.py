from django.urls import path, include
from . import views


app_name = 'esuits'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('home/', views.HomeView.as_view(), name='home'),

    #esuits_utilsの動作確認用
    path('samples/', include('esuits.samples.urls')),
    path('escreate/', views.ESCreateView.as_view(), name='es_create'),
    path('es_edit/<int:es_group_id>', views.EsEditView.as_view(), name='es_edit'),
]
