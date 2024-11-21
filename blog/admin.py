from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    # For ckeditor (PostAdminForm)
    form = PostAdminForm
    save_as = True

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'category', 'views_count', 'created_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content', 'views_count')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published', 'tags')
    readonly_fields = ('views_count', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'category', 'tags', 'created_at', 'content', 'photo', 'get_photo', 'views_count', 'is_published')
    list_per_page = 5

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Фото'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)