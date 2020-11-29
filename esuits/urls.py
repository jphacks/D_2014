# -*- coding: utf-8 -*-
from django.urls import path, include
# from .escreate import views as escreate_view
from .home import views as home_view
from .index import views as index_view
# from .esedit import views as esedit_view
from .login import views as login_view
from .signup import views as signup_view
from .tagcreate import views as tagcreate_view
from .logout import views as logout_view
from .views import DammyView as dv
from .escreate import views as escreate_view


app_name = 'esuits'
urlpatterns = [
    path('', index_view.IndexView.as_view(), name='index'),
    path('login/', login_view.LoginView.as_view(), name='login'),
    path('logout/', logout_view.logoutfunc, name='logout'),
    path('signup/', signup_view.SignupView.as_view(), name='signup'),
    path('home/', home_view.HomeView.as_view(), name='home'),
    # esの質問を登録するページ
    path('escreate/', escreate_view.ESCreateView.as_view(), name='es_create'),
    # path('escreate/', dv.as_view(), name='es_create'),
    # esを編集するページ
    path('esedit/<int:es_group_id>', dv.as_view(), name='es_edit'),
    # path('get_related/', esedit_view.get_related_post, name='get_related'),
    # path('get_wordcloud/', esedit_view.get_wordcloud_path, name='get_wordcloud'),
    # esuits_utilsの動作確認用
    path('samples/', include('esuits.samples.urls')),
    # タグ新規作成ページ
    path('tagcreate/', tagcreate_view.TagCreateView.as_view(), name='tag_create'),
]
