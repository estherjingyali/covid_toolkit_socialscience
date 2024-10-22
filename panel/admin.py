from django.contrib import admin
from import_export import resources
from .models import LoginUser,WeiboCy, WeiboTopicSA, WeiboTopicComment, WeiboComment, CovidData, SocialMediaData

# Register your models here.
admin.site.register(LoginUser)
admin.site.register(WeiboCy)
admin.site.register(WeiboTopicSA)
admin.site.register(WeiboTopicComment)
admin.site.register(WeiboComment)
admin.site.register(CovidData)
admin.site.register(SocialMediaData)

