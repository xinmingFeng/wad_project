"""wad_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from anotherplanet import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.categories, name='categories'),
                  path('index/', views.categories),
                  path('add_article/', views.add_article, name='add_article'),  # 添加文章
                  path('backend/', views.backend, name='backend'),  # 个人中心

                  path('upload_img/', views.upload_img, name='upload_img'),  # 上传Markdown文本编辑器内的图片
                  # path('',views.cat,name='cat'),
                  # path('',views.dog,name='dog'),
                  # path('',views.smallpets,name='samllpets'),
                  # path('',views.fish,name='fish'),
                  path('anotherplanet/', include('anotherplanet.urls')),
                  re_path('update_article/(?P<uid>\d+)', views.update_article),  # 文章更新
                  re_path(r'^article/(?P<id>\d+).html$', views.article_detail, name="article_detail"),  # 文章详情页
                  path('comment/', views.comment, name='comment'),  # 评论
                  path('upanddown/', views.upanddown, name='upanddown'),  # 点赞点踩
                  path('categories_list/<int:id>', views.categories_list, name="categories_list"),  # 文章列表页
                  path('get_valid_code/', views.get_valid_code, name='get_valid'),  # 获取验证码
                  path('check_username/', views.check_username, name='check_username'),  # 校验用户名是否存在
                  re_path('delete/(?P<did>\d+)', views.delete_target),  # 文章、标签、分类的删除
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
