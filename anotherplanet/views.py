from django.shortcuts import render
from django.http import HttpResponse
from anotherplanet.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import transaction
from django.contrib import auth
from django.urls import reverse
from django.db.models import F
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup

from io import BytesIO
from anotherplanet import x_forms
import markdown
import datetime
import random
import json
import time
import uuid
import re
from .models import Category
# Create your views here.
from django.core.paginator import Paginator
from anotherplanet import  models
from django.contrib.auth import get_user_model
#目录页面
def categories(request):

    context_dict={}
    category_list=Category.objects.all()
    context_dict["category_list"]=category_list
    article_list = models.Article.objects.all().order_by('-create_time')
    context_dict["article_list"]=article_list
    page_num_int = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, 6)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    start = 1
    end = paginator.num_pages
    if page_num_int > int(end):
        return redirect(reverse('error'))
    return render(request, 'anotherplanet/new_templates/Index.html', locals())

def categories_list(request,id):

    category_list = Category.objects.all()

    article_list = models.Article.objects.filter(category__id=id).order_by('-create_time')

    page_num_int = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, 6)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    start = 1
    end = paginator.num_pages
    if page_num_int > int(end):
        return redirect(reverse('error'))
    return render(request, 'anotherplanet/new_templates/article/category_list.html', locals())

# 文章添加
@login_required(login_url='/login/')
def add_article(request):
    res = {'code': 100, 'msg': '发布成功'}
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('html_doc')
        markdown = request.POST.get('mark_doc')
        category = request.POST.get('category')
        head_img = request.FILES.get('head_img')
        soup = BeautifulSoup(content, 'html.parser')
        description = soup.text[0:120]
        res_script = soup.find_all('script')
        for script in res_script:
            script.decompose()
        article = models.Article.objects.create(
            title=title,
            description=description,
            content=str(soup),
            markdown=markdown,
            category_id=category,
            head_img=head_img,
            user_id=request.user.id
        )
        return JsonResponse(res)


# 文章更新
@login_required(login_url='/login/')
def update_article(request, uid):
    if request.method == 'POST':
        res = {'code': 100, 'msg': '修改成功'}
        title = request.POST.get('title')
        content = request.POST.get('html_doc')
        markdown = request.POST.get('mark_doc')
        category = request.POST.get('category')
        head_img = request.FILES.get('head_img')
        modify_time = datetime.datetime.now()
        if not head_img:
            res['code'] = 200
            res['msg'] = '请选择图片'
            return JsonResponse(res)
        new_head_img = 'article_head_img/' + head_img.name
        img = Image.open(head_img)
        img.save('media/article_head_img/' + head_img.name)

        soup = BeautifulSoup(content, 'html.parser')
        description = soup.text[0:120]
        res_script = soup.find_all('script')
        for script in res_script:
            script.decompose()
        models.Article.objects.filter(pk=uid).update(
            title=title,
            user=request.user,
            description=description,
            content=str(soup),
            markdown=markdown,
            category_id=category,
            head_img=new_head_img,
            modify_time=modify_time
        )
        return JsonResponse(res)
    article_obj = models.Article.objects.filter(pk=uid).first()
    category_list = models.Category.objects.all()

    return render(request, 'anotherplanet/new_templates/article/Update_Article.html', locals())


# 个人中心
# 文章更新
@login_required(login_url='/login/')
def backend(request):
    article_num = models.Article.objects.filter(user=request.user).count()
    category_num = models.Category.objects.all().count()

    article_list = models.Article.objects.filter(user=request.user)
    page_num_int = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, 10)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    category_list = models.Category.objects.all()

    start = 1
    end = paginator.num_pages

    return render(request, 'anotherplanet/new_templates/user/Backend.html', locals())




# Markdown编辑器上传图片
@login_required(login_url='/login/')
def upload_img(request):
    img_obj = request.FILES.get('editormd-image-file')
    img = Image.open(img_obj)
    uid = ''.join(str(uuid.uuid4()).split('-'))[::4]
    tmp = img_obj.name.rsplit('.', 1)[-1]
    t = str(time.time()).split('.')
    img_name = ''.join([t[0], t[-1], '_', uid, '.', tmp])
    img.save('media/article_img/' + img_name)
    return JsonResponse({'success': 1, 'msg': '上传成功', 'url': f"/media/article_img/{img_name}"})


# 文章详情

def article_detail(request, id):

    article = models.Article.objects.get(id=id)
    article.views=article.views+1
    article.save()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    content = md.convert(article.markdown)
    toc = md.toc
    # article.toc = article.markdown.toc
    n = content.count('<div class="codehilite">', 0, len(content))
    for i in range(n):
        content = re.sub(r'<div class="codehilite">',
                         '<button id="ecodecopy" class="copybtn btn btn-outline-light btn-sm" '
                         'data-clipboard-action="copy" '
                         'data-clipboard-target="#code{}">复制</button> '
                         '<div class="codehilite" id="code{}">'.format(i, i), content, 1)
    comment_list = models.Comment.objects.filter(article=article)


    return render(request, 'anotherplanet/new_templates/article/Article_Detail.html', locals())





# 文章评论
@login_required(login_url='/login/')
def comment(request):
    res = {'code': 100, 'msg': ''}
    if request.is_ajax():
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        parent = request.POST.get('parent')
        if request.user.is_authenticated:
            article = models.Comment.objects.create(user=request.user, article_id=article_id, content=content,comment_id_id=parent)

            res['msg'] = '评论成功'
            res['username'] = article.user.username
            res['content'] = article.content
            if parent:
                res['parent_name'] = article.comment_id.user.username
        else:
            res['code'] = 109
            res['msg'] = '请先登录'

    return JsonResponse(res)


# 点赞点踩
@login_required(login_url='/login/')
def upanddown(request):
    res = {'code': 100, 'msg': ''}
    if request.user.is_authenticated:
        article_id = request.POST.get('article_id')
        user_id = request.user.id
        is_up = json.loads(request.POST.get('is_up'))
        article_obj = models.Article.objects.filter(pk=article_id).first()
        clicked = models.UpAndDown.objects.filter(article_id=article_id, user_id=user_id).first()
        if not request.user == article_obj.user:
            if clicked:
                res['code'] = 101
                res['msg'] = '您已经支持过' if clicked.is_up else '您已经反对过'
            else:
                with transaction.atomic():
                    models.UpAndDown.objects.create(article_id=article_id, user_id=user_id, is_up=is_up)
                    if is_up:
                        models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                        res['msg'] = '点赞成功'
                    else:
                        models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                        res['msg'] = '点踩成功'
        else:
            res['code'] = 103
            res['msg'] = '不能推荐自己的内容' if is_up else '不能反对自己的内容'
    else:
        res['code'] = 104
        res['msg'] = '请先<a href="/login/">登录</a>'
    return JsonResponse(res)









# 退出
def logout(request):
    auth.logout(request)
    return redirect(reverse('anotherplanet:login'))


# 注册
def register(request):
    if request.method == 'GET':
        form = x_forms.FormRegister()
        return render(request, 'anotherplanet/new_templates/Register.html', context={'form': form})
    elif request.method == 'POST':
        form = x_forms.FormRegister(data=request.POST)
        res = {'code': '', 'msg': ''}
        if form.is_valid():
            data = form.cleaned_data
            data.pop('re_password')
            file = request.FILES.get('avatar')
            if file:
                data['avatar'] = file
            user=get_user_model().objects.create_user( username=data["username"],email=data["email"],password=data["password"])
            models.UserProfile.objects.create(
                user=user,
                picture=data['avatar']
            )
            res['code'] = 100
            res['msg'] = '注册成功！'
            res['url'] = '/anotherplanet/login/'
            return JsonResponse(res)
        else:
            res['code'] = 101
            res['msg'] = '数据校验失败！'
            res['err'] = form.errors
            return JsonResponse(res)
    else:
        return HttpResponse('非法请求！')


# 校验用户名是否存在
def check_username(request):
    if request.method == 'GET':
        res = {'code': 101, 'msg': '该用户名已存在'}
        username = request.GET.get('username')
        if username:
            user = get_user_model().objects.filter(username=username).count()
            if not user:
                res['code'] = 100
            return JsonResponse(res)
        else:
            res['code'] = 102
            res['msg'] = '用户名不能为空'
            return JsonResponse(res)
    else:
        return HttpResponse('非法请求！')


# 登录
def login(request):
    if request.method == 'POST':
        res = {'code': 100}
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        if request.session.get('valid_code').upper() == valid_code.upper() or valid_code == '123':
            user = auth.authenticate(username=username, password=password)
            freezed = get_user_model().objects.filter(username=username, is_active=0).first()
            res['url'] = '/index/'
            if freezed:
                res['code'] = 105
                res['msg'] = '账户被冻结'
            if user:
                auth.login(request, user)
                res['msg'] = '登录成功'
            else:
                res['code'] = 101
                res['msg'] = '用户名密码错误'
        else:
            res['code'] = 102
            res['msg'] = '验证码错误'
        return JsonResponse(res)
    elif request.method == 'GET':
        form = x_forms.FormLogin()
        return render(request, 'anotherplanet/new_templates/Login.html', {'form': form})
    else:
        return HttpResponse('非法请求！')


# 获取随机颜色
def get_rgb():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# 获取验证码
def get_valid_code(request):
    img = Image.new('RGB', (200, 38), get_rgb())
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype('./static/font/FZFenSTXJW.TTF', 25)
    valid_code = ''
    for i in range(5):
        low_char = chr(random.randint(97, 122))
        num_char = random.randint(0, 9)
        upper_char = chr(random.randint(65, 90))
        res = random.choice([low_char, num_char, upper_char])
        valid_code += str(res)
        img_draw.text((i * 40 + 10, 5), str(res), get_rgb(), img_font)
    request.session['valid_code'] = valid_code
    print(valid_code)

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return HttpResponse(data)


@login_required
def restricted(request):
    return render(request, 'anotherplanet/restricted.html')



# 文章删除
@login_required(login_url='/login/')
def delete_target(request, did):
    if request.method == 'POST':
        res = {'code': 100}

        models.Article.objects.filter(id=did).delete()

        return JsonResponse(res)