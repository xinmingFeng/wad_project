from django.contrib import admin
from anotherplanet.models import UserProfile,Category


# Register your models here.





class CategoryAdmin(admin.ModelAdmin):
    list_display =('id','name')



admin.site.register(UserProfile)
admin.site.register(Category,CategoryAdmin)