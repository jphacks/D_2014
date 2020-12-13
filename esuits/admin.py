from django.contrib import admin
from .models import CustomUserModel, TagModel, ESGroupModel, PostModel

# Register your models here.
admin.site.register(CustomUserModel)
admin.site.register(TagModel)
admin.site.register(ESGroupModel)
admin.site.register(PostModel)