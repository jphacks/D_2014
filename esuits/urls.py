# -*- coding: utf-8 -*-
from django.urls import path, include
# from .escreate import views as escreate_view
from .home.views import HomeView
from .index.views import IndexView
from .esedit.views import EsEditView
from .login.views import LoginView
from .signup.views import SignupView
from .tagcreate.views import TagCreateView
from .logout.views import logoutfunc
from .escreate.views import ESCreateView
from .question_list.views import QuestionListView
from .esedit.views import get_related_post, get_wordcloud_path


app_name = 'esuits'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('home/', HomeView.as_view(), name='home'),
    # esの質問を登録するページ
    path('escreate/', ESCreateView.as_view(), name='es_create'),
    # esを編集するページ
    path('esedit/<int:es_id>', EsEditView.as_view(), name='es_edit'),
    path('get_related/', get_related_post, name='get_related'),
    path('get_wordcloud/', get_wordcloud_path, name='get_wordcloud'),
    # esuits_utilsの動作確認用
    path('samples/', include('esuits.samples.urls')),
    # タグ新規作成ページ
    path('tagcreate/', TagCreateView.as_view(), name='tag_create'),
    # 質問一覧表示ページ
    path('questions/', QuestionListView.as_view(), name='questions'),
]
