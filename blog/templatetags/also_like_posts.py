from django import template
from blog.models import Post, Tag

register = template.Library()

@register.inclusion_tag('blog/inc/also_like_posts_tmp.html')
def get_also_like_posts(self, count=3):
    posts = Post.objects.filter(is_published=True, category=self.object.category).exclude(id=self.object.id)[:count]
    return {'also_like_posts': posts}
