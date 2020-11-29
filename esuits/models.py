# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUserModel(AbstractUser):
    '''ユーザーテーブル'''

    class Meta(object):
        db_table = 'custom_users'

    def __str__(self):
        return self.username


class TagModel(models.Model):
    '''タグテーブル'''

    class Meta(object):
        db_table = 'tags'

    tag_name = models.CharField(verbose_name='タグ名', max_length=255)
    authors = models.ManyToManyField(CustomUserModel, verbose_name='作成者')

    def __str__(self):
        return self.tag_name


class CompanyModel(models.Model):
    '''企業テーブル'''

    class Meta(object):
        db_table = 'companies'

    company_name = models.CharField(verbose_name='企業名', max_length=100)

    def __str__(self):
        return self.company_name


class CompanyHomepageURLModel(models.Model):
    # WordCloudModel→
    '''企業URLテーブル'''

    class Meta(object):
        db_table = 'homepage_urls'

    company = models.ForeignKey(CompanyModel, verbose_name='企業', on_delete=models.CASCADE)
    homepage_url = models.URLField(verbose_name='企業URL', max_length=200)
    word_cloud_path = models.CharField(verbose_name='ワードクラウドパス', max_length=255)

    def __str__(self):
        return self.homepage_url


class EntrySheetesModel(models.Model):
    # ESGroupModel→
    '''エントリーシートテーブル'''

    class Meta(object):
        db_table = 'entry_sheets'

    company = models.ForeignKey(CompanyModel, verbose_name='企業 ',
                                on_delete=models.CASCADE, null=True, blank=True)
    homepage_url = models.ForeignKey(
        CompanyHomepageURLModel, verbose_name='ホームページURL', on_delete=models.CASCADE, null=True, blank=True)
    selection_type = models.CharField(verbose_name='選考種別', max_length=50, blank=True, null=True)
    author = models.ForeignKey(CustomUserModel, verbose_name='作成者', on_delete=models.CASCADE)
    is_editing = models.BooleanField(verbose_name='作成中or完成', default=True)
    created_date = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    deadline_date = models.DateTimeField(
        verbose_name='提出期限', default=timezone.now, blank=True, null=True)

    def __str__(self):
        if self.selection_type is None:
            return self.company.company_name + '_none'
        else:
            return self.company.company_name + '_' + self.selection_type


class QuestionModel(models.Model):
    # PostModel→
    '''質問デーブル'''

    class Meta(object):
        db_table = 'questions'

    entry_sheet = models.ForeignKey(
        EntrySheetesModel, on_delete=models.CASCADE, verbose_name='エントリーシート')
    question = models.TextField(verbose_name='質問')
    answer = models.TextField(verbose_name='', blank=True, null=True)
    tags = models.ManyToManyField(TagModel, verbose_name='タグ名', null=True, blank=True)
    char_num = models.IntegerField(default=0, blank=True)
    OPEN_INFO_CHOICES = [
        ('public', '公開'),
        ('private', '非公開')
    ]
    open_info = models.CharField(verbose_name='公開or非公開', max_length=20,
                                 choices=OPEN_INFO_CHOICES, default='private')

    def __str__(self):
        return self.question
