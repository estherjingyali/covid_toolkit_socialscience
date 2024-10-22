# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def _create_user(self, name, password, **kwargs):
        if not name:
            raise ValueError("Please enter your username！")
        if not password:
            raise ValueError("Please enter your password！")
        user = self.model(name=name, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, **kwargs)


class LoginUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=128)
    password = models.CharField(max_length=256)
    sex = models.CharField(max_length=32)
    c_time = models.DateField()
    has_confirmed = models.IntegerField()
    is_staff = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=True)

    NAME_FIELD = 'name'

    objects = UserManager()

    class Meta:
        db_table = 'login_user'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class WeiboCy(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.TextField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '微博词云数据'


class ProvincialData(models.Model):
    date = models.FloatField(blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    confirm = models.IntegerField(blank=True, null=True)
    dead = models.IntegerField(blank=True, null=True)
    heal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '全国疫情情况'


class PrefectureData(models.Model):
    date = models.FloatField(blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    confirm = models.IntegerField(blank=True, null=True)
    dead = models.IntegerField(blank=True, null=True)
    heal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '各省疫情情况'


class NewData(models.Model):
    date = models.FloatField(blank=True, null=True)
    confirm = models.IntegerField(blank=True, null=True)
    suspect = models.IntegerField(blank=True, null=True)
    dead = models.IntegerField(blank=True, null=True)
    heal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '新增人数'


class WeiboTopicSA(models.Model):
    id = models.IntegerField(primary_key=True)
    topic = models.TextField(blank=True, null=True)
    positive = models.IntegerField(blank=True, null=True)
    negative = models.IntegerField(blank=True, null=True)
    neutral = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '微博疫情评论分析结果'


class WeiboTopicComment(models.Model):
    id = models.IntegerField(primary_key=True)
    topic = models.TextField(db_column='话题', blank=True, null=True)
    commend = models.TextField(db_column='评论', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '微博疫情话题评论'


class WeiboComment(models.Model):
    id = models.IntegerField(primary_key=True)
    article_url = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    title_user_id = models.BigIntegerField(blank=True, null=True)
    title_user_nicname = models.CharField(db_column='title_user_NicName', max_length=256, blank=True,
                                          null=True)  # Field name made lowercase.
    title_user_gender = models.CharField(max_length=32, blank=True, null=True)
    reposts_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    attitudes_count = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '微博评论数据'


class CovidData(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.FloatField(blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    p_confirm = models.IntegerField(blank=True, null=True)
    p_dead = models.IntegerField(blank=True, null=True)
    p_heal = models.IntegerField(blank=True, null=True)
    date_1_field = models.FloatField(db_column='date (1)', blank=True,
                                     null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    province_1_field = models.CharField(db_column='province (1)', max_length=255, blank=True,
                                        null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    city = models.CharField(max_length=255, blank=True, null=True)
    c_confirm = models.IntegerField(blank=True, null=True)
    c_dead = models.IntegerField(blank=True, null=True)
    c_heal = models.IntegerField(blank=True, null=True)
    date_latest60d = models.FloatField(db_column='date（latest60day', blank=True,
                                  null=True)  # Field renamed to remove unsuitable characters.
    n_confirm = models.IntegerField(blank=True, null=True)
    n_dead = models.IntegerField(blank=True, null=True)
    n_heal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '疫情数据表'


class SocialMediaData(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.FloatField(blank=True, null=True)
    article_url = models.CharField(max_length=255, blank=True, null=True)
    title_user_id = models.CharField(max_length=255, blank=True, null=True)
    title_user_nicname = models.CharField(db_column='title_user_NicName', max_length=255, blank=True,
                                          null=True)  # Field name made lowercase.
    title_user_gender = models.CharField(max_length=32, blank=True, null=True)
    reposts_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    attitudes_count = models.IntegerField(blank=True, null=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    positive = models.IntegerField(blank=True, null=True)
    negative = models.IntegerField(blank=True, null=True)
    neutral = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '社交网络数据表'
