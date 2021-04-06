from django.urls import path
from anotherplanet import views


app_name = 'anotherplanet'

urlpatterns = [
    path('', views.categories, name='categories'),
    # path('cat/',views.cat,name='cat'),
    # path('dog/',views.dog,name='dog'),
    # path('smallpets/',views.smallpets,name='smallpets'),
    # path('fish/',views.fish,name='fish'),
    path('register/',views.register, name='register'),
    path('login/', views.login,name='login'),
    path('restricted/',views.restricted, name='restricted'),
    path('logout/', views.logout, name='logout'),
]