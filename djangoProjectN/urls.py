"""djangoProjectN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from panel.views import index, login, register, logout, analyse, cptable, cttable, newtable, weibocomment, weiboword, visitor, search, correlation,ttest,anova,regression,dataimport
from django.views.static import serve
from djangoProjectN.settings import MEDIA_ROOT

urlpatterns = [
   path('admin/', admin.site.urls),
   path('index/', index, name='index'),
   path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('analyse/', analyse, name='analyse'),
    path('correlation', correlation, name="correlation"),
    path('ttest', ttest, name='ttest'),
    path('anova', anova, name='anova'),
    path('regression', regression, name='regression'),
    path('cptable/', cptable, name='cptable'),
    path('cttable/', cttable, name='cttable'),
    path('newtable/', newtable, name='newtable'),
    path('weibocomment/', weibocomment, name='weibocomment'),
    path('weiboword/', weiboword, name='weiboword'),
    path('visitor/', visitor, name='visitor'),
    path('search/<str:column>/<str:kw>', search, name='search'),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}, name='media'),
    path('dataimport', dataimport, name='DataImport'),
]
