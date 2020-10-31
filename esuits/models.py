from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

# Create your models here.


class CustomUserModel(AbstractUser):
    '''カスタムユーザークラス'''
    class Meta(object):
        db_table = 'custom_user'

    def __str__(self):
        return self.username


class TagModel(models.Model):
    '''タグモデル'''

    class Meta(object):
        db_table = 'tag_table'

    tag_name = models.CharField(verbose_name='タグ名', max_length=255)
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_name


class ESGroupModel(models.Model):
    class Meta(object):
        db_table = 'esgroup_table'

    company = models.CharField(verbose_name='会社名', max_length=100)
    event_type = models.CharField(verbose_name='イベントタイプ', max_length=50, blank=True, null=True)
    company_url = models.URLField(verbose_name='企業ホームページ', max_length=200)
    author = models.ForeignKey(CustomUserModel, verbose_name='作成者', on_delete=models.CASCADE)
    is_editing = models.BooleanField(verbose_name='作成中', default=True)
    created_date = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    def __str__(self):
        return self.event_name


class PostModel(models.Model):
    class Meta(object):
        db_table = 'post_table'

    question = models.TextField(verbose_name='質問')
    answer = models.TextField(verbose_name='回答')
    # create_date = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    tags = models.ManyToManyField(TagModel, verbose_name='タグ名', blank=True)

    # OPEN_INFO_CHOICES = [
    #     ('public', '公開'),
    #     ('private', '非公開')
    # ]
    # open_info = models.CharField(verbose_name='公開', max_length=20,
    #                              choices=OPEN_INFO_CHOICES, default='private')
    # company = models.CharField(verbose_name='会社名', max_length=50, blank=True, null=True)
    # state = models.CharField(verbose_name='状況', max_length=50, blank=True, null=True)
    # author = models.ForeignKey(CustomUserModel, verbose_name='ユーザ名', on_delete=models.CASCADE)
    es_group_id = models.ForeignKey(ESGroupModel, verbose_name='es名', on_delete=models.CASCADE)
    char_num = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.question
