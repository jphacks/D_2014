from django.contrib import admin
from .models import CompanyModel, CompanyHomepageURLModel, EntrySheetesModel, TagModel, CustomUserModel, QuestionModel

# Register your models here.
admin.site.register(CustomUserModel)
admin.site.register(TagModel)
admin.site.register(CompanyModel)
admin.site.register(CompanyHomepageURLModel)
admin.site.register(EntrySheetesModel)
admin.site.register(QuestionModel)
