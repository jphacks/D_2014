from django.urls import path, include
from . import views
from .shinkiSakusei import views as shinkisakusei_view


app_name = 'esuits'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('home/', views.HomeView.as_view(), name='home'),
    # esの質問を登録するページ
    path('escreate/', views.ESCreateView.as_view(), name='es_create'),
    # esを編集するページ
    path('es_edit/<int:es_group_id>', views.EsEditView.as_view(), name='es_edit'),

    # 新規作成ページ
    path('shinkiSakusei/', shinkisakusei_view.SinkiSakuseiView.as_view(), name='shinkiSakusei'),

    # esuits_utilsの動作確認用
    path('samples/', include('esuits.samples.urls')),

    # タグ新規作成ページ
    path('tagcreate/', views.TagCreateView.as_view(), name='tag_create'),
]
