from django.contrib import admin
from .models import *


@admin.register(Product)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", 'slug')


@admin.register(Category)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", 'slug')


@admin.register(Subcategory)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", 'slug')


admin.site.register(Provider)
admin.site.register(Feedback)
admin.site.register(AnimalSort)
admin.site.register(Basket)
