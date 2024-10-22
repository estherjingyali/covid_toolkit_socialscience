import os
import random
import sys
import base64
from io import BytesIO
import environ
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from statannotations.Annotator import Annotator

import warnings

from djangoProjectN.settings import BASE_DIR

warnings.filterwarnings("ignore")
from pyforest import *

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine


from . import models
from . import forms
import hashlib
import datetime
import csv
import pymysql.cursors
import json
import pandas as pd


env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DATABASE_URL = f"mysql+pymysql://{env('DB_USER')}:{env('DB_PWD')}@127.0.0.1:3306/poavs"
ENGINE = create_engine(DATABASE_URL)


def hash_code(s, salt='djangoProjectN'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code

def login(request):
    if request.session.get('is_login', None):  # not allowed multi-panel
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'Please check the content!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.LoginUser.objects.get(name=username)
            except:
                message = 'This username does not exist！'
                return render(request, 'panelviews/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = 'Error!Password'
                return render(request, 'panelviews/login.html', locals())
        else:
            return render(request, 'panelviews/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'panelviews/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "Please check the content！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = 'Different with the ori password！'
                return render(request, 'panelviews/register.html', locals())
            else:
                same_name_user = models.LoginUser.objects.filter(name=username)
                if same_name_user:
                    message = 'This username already exists!'
                    return render(request, 'panelviews/register.html', locals())

                new_user = models.LoginUser()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'panelviews/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'panelviews/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")


def visitor(request):

    return render(request, 'panelviews/visitor.html')


@csrf_exempt
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    try:
        if request.GET:
            date = request.GET['date']
        else:
            date = '2022-05-11'
    except:
        date = '2022-05-11'

    try:
        type = request.GET['out']
    except:
        type = 'in'

    with open(r'D:/djangoProjectN/panel/csvfiles/微博词云数据.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        date2, comment2, num2 = [], [], []
        for row in reader:
            date2.append(row[0])
            comment2.append(row[1])
            num2.append(row[2])

    cy_date = date[-2:]
    cy_date = str(int(cy_date))
    index = int(cy_date) - 1
    if type != 'in':
        cy_comment = eval(comment2[index])
        cy_num = eval(num2[index])
    else:
        cy_comment = eval(comment2[index])
        cy_num = eval(num2[index])

    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='poavs', charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 微博疫情评论分析结果")
    results = cursor.fetchall()
    topic, positive, negative, neutral =[], [], [], []
    for row in results:
        topic.append(row[1])
        positive.append(int(row[2]))
        negative.append(int(row[3]))
        neutral.append(int(row[4]))

    date = date[5:7] + '.' + date[-2:]

    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='poavs', charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM 全国疫情情况")
    results = cursor.fetchall()
    date1, province, confirm, dead, heal = [], [], [], [], []
    for row in results:
        date1.append(row[0])
        province.append(row[1])
        confirm.append(int(row[2]))
        dead.append(int(row[3]))
        heal.append(int(row[4]))
    index = []
    for i in range(len(date1)):
        if date1[i] == date:
            index.append(i)
    map_province, map_confirm, map_dead, map_heal = [], [], [], []
    for i in index:
        map_province.append(province[i])
        map_confirm.append(confirm[i])
        map_dead.append(int(dead[i]))
        map_heal.append(int(heal[i]))


    name = '福建'
    date11 = '05.11'
    if request.POST:
        name = request.POST['name']
        date1 = random.randint(10, 30)
        date11 = '05.' + str(date1)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM 各省疫情情况")
    results = cursor.fetchall()
    date1, province, city, confirm, dead, heal = [], [], [], [], [], []
    for row in results:
        date1.append(row[0])
        province.append(row[1])
        city.append(row[2])
        confirm.append(int(row[3]))
        dead.append(int(row[4]))
        heal.append(int(row[5]))
    index = []
    for i in range(len(date1)):
        if date1[i] == date11:
            index.append(i)
    city_name = []
    city_confirm = []
    for i in index:
        if province[i] == name:
            city_name.append(city[i])
            city_confirm.append(confirm[i])

    cursor = db.cursor()
    cursor.execute("SELECT * FROM 新增人数")
    results = cursor.fetchall()
    date, confirm, dead, heal = [], [], [], []
    for row in results:
        date.append(row[0])
        confirm.append(int(row[1]))
        dead.append(int(row[3]))
        heal.append(int(row[4]))

    return render(request, 'panelviews/index.html', {'date':json.dumps(date), 'confirm': json.dumps(confirm), 'dead': json.dumps(dead), 'heal': json.dumps(heal), 'map_province': json.dumps(map_province, ensure_ascii=False), 'map_confirm': json.dumps(map_confirm), 'city_name': json.dumps(city_name, ensure_ascii=False), 'city_confirm': json.dumps(city_confirm), 'name': json.dumps(name, ensure_ascii=False), 'topic': json.dumps(topic), 'positive': json.dumps(positive), 'negative': json.dumps(negative), 'neutral': json.dumps(neutral), 'cy_num': json.dumps(cy_num), 'cy_comment': json.dumps(cy_comment)})





TABLE_M_SELECT = {
    '日期（省级累计）': 'date',
    '省份（省级累计）': 'province',
    '确诊人数（省级累计）': 'p_confirm',
    '死亡人数（省级累计）': 'p_dead',
    '治愈人数（省级累计）': 'p_heal',
    '日期（市级累计）': 'date(1)',
    '省份（市级累计）': 'province(1)',
    '城市': 'city',
    '确诊人数（市级累计）': 'c_confirm',
    '死亡人数（市级累计）': 'c_dead',
    '治愈人数（市级累计）': 'c_heal',
    '日期（近60天新增）': 'date（近60天',
    '确诊人数（近60天新增）': 'n_confirm',
    '死亡人数（近60天新增）': 'n_dead',
    '治愈人数（近60天新增）': 'n_heal',
}




@csrf_exempt
def analyse(request):
    sql = "Select * from 新增人数"
    df = pd.read_sql_query(sql, ENGINE)
    table = df.to_html(classes='ui selectable celled table',
                         table_id='table')
    mselect_dict = {}
    for key, value in TABLE_M_SELECT.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        # mselect_dict[key]['options'] = option_list

    context = {
        'table': table,
        'mselect_dict': mselect_dict
    }

    return render(request, 'panelviews/analyse.html', context)


def correlation(request):
        df = pd.read_csv(r"/panel/csvfiles/疫情数据表.csv", encoding='utf-8')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False  # 减号-unicode编码
        corr = df.corr()
        matplotlib.use('Agg')
        ax = plt.subplots(figsize=(14, 6))  # adjust canvas size
        sns.heatmap(corr, vmax=.8, square=True, annot=True)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        sio = BytesIO()
        plt.savefig('plot1.pdf')
        plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
        plot_url = base64.encodebytes(sio.getvalue()).decode()
        args = {"plot_url": plot_url}
        plt.close()
        return render(request, 'panelviews/correlation.html', args)


def ttest(request):
    df = pd.read_csv(r"/panel/csvfiles/社交网络数据表.csv", encoding='utf-8')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    data_p = df[["title_user_gender","reposts_count"]]
    order = ['m','f']
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100, facecolor="w")
    ax = sns.barplot(x="title_user_gender", y="reposts_count", data=data_p,
                     estimator=np.mean, ci="sd", capsize=.1, errwidth=1, errcolor="k",
                     ax=ax, order=order,
                     **{"edgecolor": "k", "linewidth": 1})

    pairs=[("m","f")]
    annotator = Annotator(ax, pairs, data=data_p, x="title_user_gender", y="reposts_count")
    annotator.configure(test='Mann-Whitney', text_format='star', line_height=0.03, line_width=1)
    annotator.apply_and_annotate()

    ax.tick_params(which='major', direction='in', length=3, width=1., labelsize=14, bottom=False)
    for spine in ["top", "left", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.grid(axis='y', ls='--', c='gray')
    ax.set_axisbelow(True)
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    plt.savefig('plot2.pdf')
    plot_url = base64.encodebytes(sio.getvalue()).decode()
    args = {"plot_url": plot_url}
    plt.close()
    return render(request, 'panelviews/ttest.html', args)

def anova(request):
    df = pd.read_csv(r"/panel/csvfiles/假设检验.csv", encoding='utf-8')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    data_p = df[["emotion","value"]]
    order = ['positive', 'negative','neutral']
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100, facecolor="w")
    ax= sns.boxplot(data=data_p,x="emotion",y="value",order=order,ax=ax)
    pairs=[("positive","negative"),("negative","neutral"),("positive","neutral")]
    annotator=Annotator(ax,pairs,data=data_p,x="emotion",y="value",order=order)
    annotator.configure(test='t-test_ind', text_format='star', line_height=0.03, line_width=1)
    annotator.apply_and_annotate()

    ax.tick_params(which='major', direction='in', length=3, width=1., labelsize=14, bottom=False)
    for spine in ["top", "left", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.grid(axis='y', ls='--', c='gray')
    ax.set_axisbelow(True)
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    plt.savefig('plot3.pdf')
    plot_url = base64.encodebytes(sio.getvalue()).decode()
    args = {"plot_url": plot_url}
    plt.close()
    return render(request, 'panelviews/anova.html', args)


def regression(request):
    df = pd.read_csv(r"/panel/csvfiles/疫情数据表.csv", encoding='utf-8')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    data_p = df[["p_confirm", "p_heal"]]
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100, facecolor="w")
    ax = sns.regplot(data=data_p, x="p_confirm", y="p_heal",ax=ax)

    ax.tick_params(which='major', direction='in', length=3, width=1., labelsize=14, bottom=False)
    for spine in ["top", "left", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.grid(axis='y', ls='--', c='gray')
    ax.set_axisbelow(True)
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    plot_url = base64.encodebytes(sio.getvalue()).decode()
    plt.savefig('plot4.pdf')
    args = {"plot_url": plot_url}
    plt.close()

    export = request.GET.get('DataExport', 1)
    if export != 1:
        os.system('python D:/djangoProjectN/panel/pythonfiles/pdfmake.py')

    return render(request, 'panelviews/regression.html', args)


@csrf_exempt
def search(request, column, kw):
    sql = "SELECT DISTINCT %s FROM %s WHERE %s like '%%%s%%'" % (column, 'table1', 'column', kw)
    try:
        df = pd.read_sql_query(sql, ENGINE)
        l = df.values.flatten().tolist()
        results_list = []
        for element in l:
            option_dict = {'name': element,
                           'value': element,
                           }
            results_list.append(option_dict)
        res = {
            "success": True,
            "results": results_list,
            "code": 200,
        }
    except Exception as e:
        res = {
            "success": False,
            "errMsg": e,
            "code": 0,
        }
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式


@csrf_exempt
def cptable(request):
    sql = "Select * from 全国疫情情况"
    df = pd.read_sql_query(sql, ENGINE)
    table = df.to_html(classes='ui selectable celled table',
                       table_id='cptable')
    mselect_dict = {}
    for key, value in TABLE_M_SELECT.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        # mselect_dict[key]['options'] = option_list

    context = {
        'cptable': table,
        'mselect_dict': mselect_dict
    }

    crawler = request.GET.get('crawler1', 1)
    if crawler != 1:
        os.system('python D:/djangoProjectN/panel/pythonfiles/全国疫情数据爬取.py')

    return render(request, 'panelviews/cptable.html', context)



@csrf_exempt
def cttable(request):
    sql = "Select * from 各省疫情情况"
    df = pd.read_sql_query(sql, ENGINE)
    table = df.to_html(classes='ui selectable celled table',
                       table_id='cttable')
    mselect_dict = {}
    for key, value in TABLE_M_SELECT.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        # mselect_dict[key]['options'] = option_list

    context = {
        'cttable': table,
        'mselect_dict': mselect_dict
    }


    return render(request, 'panelviews/cttable.html', context)


@csrf_exempt
def newtable(request):
    sql = "Select * from 新增人数"
    df = pd.read_sql_query(sql, ENGINE)
    table = df.to_html(classes='ui selectable celled table',
                       table_id='newtable')

    mselect_dict = {}
    for key, value in TABLE_M_SELECT.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        # mselect_dict[key]['options'] = option_list

    context = {
        'newtable': table,
        'mselect_dict': mselect_dict
    }

    crawler = request.GET.get('crawler2', 1)
    if crawler != 1:
        os.system('python D:/djangoProjectN/panel/pythonfiles/疫情每日新增人数爬取.py')

    return render(request, 'panelviews/newtable.html', context)


@csrf_exempt
def weibocomment(request):
    sql = "Select * from 微博评论数据"
    df = pd.read_sql_query(sql, ENGINE)
    table = df.to_html(classes='ui selectable celled table',
                       table_id='weibocomment')

    context = {
        'weibocomment': table,
    }
    return render(request, 'panelviews/weibocomment.html', context)


@csrf_exempt
def weiboword(request):
    sql = "Select * from 微博词云数据"
    df = pd.read_sql_query(sql, ENGINE)
    table = df.to_html(classes='ui selectable celled table',
                       table_id='weiboword')

    context = {
        'weiboword': table,
    }
    return render(request, 'panelviews/weiboword.html', context)



def dataimport(request):
    data={}
    if request.method == "POST":
        upload_file = request.FILES.get("uploadfile")
        file_name = os.path.splitext(upload_file.name)
        print(file_name)
        print(upload_file.name)
        print(upload_file.size)
        fs = FileSystemStorage()
        filename = fs.save(upload_file.name, upload_file)
        data = {
            "file_data": "http://127.0.0.1:8001" + str(fs.url(filename))}
    return render(request, 'panelviews/analyse.html', context=data)






