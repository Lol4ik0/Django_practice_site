from ckeditor_uploader.forms import SearchForm
from django.db.models import Count, F, Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

# Additionally
from django.contrib import messages                                 # Сообщения которые будут выводиться пользователю на странице - https://docs.djangoproject.com/en/5.0/ref/contrib/messages/
from django.core.mail import EmailMessage

# Files
from .models import *
from .forms import SendBackEmailForm
from logging_config import *


logger = logging.getLogger(__name__)
configure_logging()


class HomePost(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'

    # paginate_orphans = 3
    # paginate_by = 6

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'DevBlog - Personal Blog Template'
        context['posts'] = Post.objects.filter(is_published=True).order_by('-views_count')
        context['categories'] = Category.objects.annotate(count_posts=Count('posts')).filter(count_posts__gt=0)
        context['tags'] = Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views_count = F('views_count') + 1
        self.object.save()
        self.object.refresh_from_db()   # This is for display views_count as number, not as "F(views_count) + Value(1)"
        context['title'] = self.object.title
        context['include_link'] = f'blog/singles/_{self.object.slug}.html'
        context['single_post'] = self
        # context['also_like_posts'] = Post.objects.filter(is_published=True, category=self.object.category).exclude(title=self.object.title)
        return context


class Filter(ListView):
    template_name = 'blog/filter.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.GET.get('all_categories') == 'on':
            if not self.request.GET.get('select_tags'):
                return Post.objects.all().order_by(self.request.GET.get('select_sorting'))
            else:
                return Post.objects.filter(tags__id__in=self.request.GET.getlist('select_tags')).order_by(self.request.GET.get('select_sorting'))

        if not self.request.GET.get('select_tags'):
            return Post.objects.filter(category_id__in=self.request.GET.getlist('select_categories')).order_by(self.request.GET.get('select_sorting'))

        return Post.objects.filter(tags__id__in=self.request.GET.getlist('select_tags')).filter(category_id__in=self.request.GET.getlist('select_categories')).order_by(self.request.GET.get('select_sorting'))

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'DevBlog - Filter'
        context['categories'] = Category.objects.annotate(count_posts=Count('posts')).filter(count_posts__gt=0)
        context['tags'] = Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sear'
        return context



def about(request):
    return render(request, 'blog/about.html', {'title': 'My blog'})


def work(request):
    return render(request, 'blog/work.html', {'title': 'My blog'})


def contact(request):
    # if not request.user.is_authenticated:
    #     messages.error(request, 'You are not authenticated! Please login first')
    #     return redirect('login')

    form = SendBackEmailForm()
    logger.info('form')
    if request.method == 'POST':
        form = SendBackEmailForm(request.POST)
        logger.info('POST')
        if form.is_valid():

            logger.info('is_valid')
            try:
                email = EmailMessage(
                    subject=form.cleaned_data['subject'],
                    body=f"Від кого: {form.cleaned_data['user_name']}\n"    +
                         f"Website: {form.cleaned_data['website']}\n"       +
                         f"Звідки: {form.cleaned_data['where_from']}\n"     +
                         f"Від кого2: {form.cleaned_data['email']}\n"       +
                         form.cleaned_data['message_content'],
                    from_email='dania.tenditnyi@demomailtrap.com',
                    to=['dania.tenditnyi@gmail.com']
                )
                email.send()
                logger.info('Email sent')

                # If we need to add some attachments to our email
                # with open(attachments/Attachment.pdf) as file:
                #     email.attach('Attachment.pdf', file.read(), 'application/pdf')
            except Exception as e:
                messages.error(request, f'Листа НЕ надіслано! Помилка: {e}')
            else:
                messages.success(request, 'Листа надіслано!')

            return redirect('contact')
        else:
            messages.error(request, 'Форма неправильно заповнена!')

    return render(request, 'blog/contact.html', {'form': form})

