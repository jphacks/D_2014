from django.urls import path, include
from . import views
from .shinkiSakusei import views as shinkisakusei_view
from .escreate import views as escreate_view
from .home import views as home_view
from .index import views as index_view
from .esedit import views as esedit_view
from .login import views as login_view
from .signup import views as signup_view
from .tagcreate import views as tagcreate_view

app_name = 'esuits'
urlpatterns = [
    path('', index_view.IndexView.as_view(), name='index'),
    path('login/', login_view.LoginView.as_view(), name='login'),
    path('signup/', signup_view.SignupView.as_view(), name='signup'),
    path('home/', home_view.HomeView.as_view(), name='home'),
    # esの質問を登録するページ
    path('escreate/', escreate_view.ESCreateView.as_view(), name='es_create'),
    # esを編集するページ
    path('es_edit/<int:es_group_id>', esedit_view.EsEditView.as_view(), name='es_edit'),

    # 新規作成ページ
    path('shinkiSakusei/', shinkisakusei_view.SinkiSakuseiView.as_view(), name='shinkiSakusei'),

    # esuits_utilsの動作確認用
    path('samples/', include('esuits.samples.urls')),

    # タグ新規作成ページ
    path('tagcreate/', tagcreate_view.TagCreateView.as_view(), name='tag_create'),
]
