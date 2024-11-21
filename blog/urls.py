from django.urls import path
from django.views.decorators.cache import cache_page    # Кеширование страниц: https://djangodoc.ru/3.2/topics/cache/

from .views import *

urlpatterns = [
    path('',                    HomePost.as_view(),     name='home'),
    path('about',               about,                  name='about'),
    path('contact',             contact,                name='contact'),
    path('work',                work,                   name='work'),
    path('post/<slug:slug>/',   GetPost.as_view(),      name='view_post'),
    path('filter/',             Filter.as_view(),       name='filter'),
    path('search/',             Search.as_view(),       name='search'),
]
