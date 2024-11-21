from django.db import models
from django.urls import reverse

# Create your models here.

"""
Category
========
title, slug

Tag 
========
title, slug

Post
========
title, slug, content, photo, category, tags, created_at, updated_at, views_count, is_published

"""

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Назва')
    slug = models.SlugField(max_length=100, verbose_name='Url', unique=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Категорія(ю)'
        verbose_name_plural = 'Категорії'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(unique=True, max_length=255, verbose_name='Url')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категорія')
    content = models.TextField(blank=True, verbose_name='Вміст')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    views_count = models.IntegerField(default=0, verbose_name='Кількість переглядів')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата останнього оновлення')
    is_published = models.BooleanField(default=True, verbose_name='Чи опублікована новина')

    def get_absolute_url(self):
        return reverse('view_post', kwargs={"slug": self.slug})

    def __str__(self):
        return f"Пост: '{self.title}', за категорією: '{self.category}'"

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['views_count']
