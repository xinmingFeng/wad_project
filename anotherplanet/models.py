from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)
    def __str__(self):
        return self.user.username

# 文章表
class Article(models.Model):
    id=models.AutoField(primary_key=True,verbose_name="序号")
    head_img = models.FileField(upload_to='article_head_img/', default='article_head_img/default_head.png',verbose_name='头图',help_text='文章的头图')
    title = models.CharField(max_length=32, verbose_name='标题', help_text='文章的标题')
    content = models.TextField(verbose_name='内容', help_text='文章的内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='该文章的创建时间')
    up_num = models.IntegerField(default=0, verbose_name='点赞数', help_text='该文章的点赞数')
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, verbose_name='文章作者')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='分类',help_text='该文章属于哪个分类')
    description = models.CharField(max_length=128, verbose_name='摘要', help_text='简要描述该文章')
    markdown = models.TextField(verbose_name='Markdown内容', default='暂无', help_text='文章的Markdown内容')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间', help_text='该文章的最后修改时间')
    views=models.PositiveIntegerField(verbose_name="浏览数",null=True,blank=True,default=0)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = '文章'
        ordering = ['id', ]

# 分类表
class Category(models.Model):
    id=models.AutoField(primary_key=True,verbose_name="序号")
    name = models.CharField(max_length=32, verbose_name='分类', help_text='分类的名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '分类'


# 评论表
class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, verbose_name='用户', help_text='该评论来自哪个用户')
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, null=True, verbose_name='文章',help_text='评论的对象是哪篇文章')
    content = models.CharField(max_length=256, verbose_name='内容', help_text='评论的内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='时间', help_text='评论的时间')
    comment_id = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, verbose_name='评论id',help_text='对哪个id的评论进行评论')
    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论'


# 点赞点踩
class UpAndDown(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='用户', help_text='来自哪个用户')
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, null=True, verbose_name='文章',help_text='针对哪篇文章')
    is_up = models.BooleanField(null=True, verbose_name='点赞点踩', help_text='True为点赞，False为点踩')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='点赞点踩的时间')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = '点赞点踩'