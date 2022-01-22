from django.contrib import admin
from rango.models import Category, Page

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'views', 'likes', 'slug'] # 可更改展示表单中显示字段的顺序
    list_display = ('name', 'views', 'likes') # 可更改列表显示的字段
    prepopulated_fields = {'slug': ('name', )} # 预处理slug field
    
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

# Register your models here.
