from django.db.models.functions import TruncMonth
from django.template import library
from django.db.models import Count
from anotherplanet import models

register = library.Library()


# 侧边栏inclusion_tag
@register.inclusion_tag('anotherplanet/new_templates/Left.html')
def left():

    res_category = models.Category.objects.all().annotate(num=Count('article__id')).values_list(
        'name', 'num', 'id')

    res_date = models.Article.objects.all().annotate(month=TruncMonth('create_time')).values(
        'month').annotate(c=Count('id')).order_by('-month').values_list('month', 'c')

    return { 'res_category': res_category,  'res_date': res_date}
