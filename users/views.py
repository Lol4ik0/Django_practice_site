import logging

from django.http import HttpResponse

from logging_config import configure_logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, RedirectView, UpdateView, DeleteView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, SendBackEmailForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.hashers import check_password
from .models import Users

# Создание и конфигурация логинга
logger = logging.getLogger(__name__)
configure_logging()


class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('')
    template_name = 'users/signup.html'

    # Set user Group on registration
    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # logger.info(f"New user created, form.cleaned_data: {form.cleaned_data}")
            logger.info(f"New user created, user: {user.__dict__}")

            # Auto-fill
            user.first_name = user.pib.split()[1]
            user.last_name = user.pib.split()[0]

            user.save()
            login(request, user)

            # One user Group
            # user_group = Group.objects.get(name='Користувач')
            # user.groups.add(user_group)

            # Multiple user Groups
            # for form_ug in form.cleaned_data['groups']:
            #     user_group = Group.objects.get(name=form_ug.name)
            #     user.groups.add(user_group)

            messages.success(request, 'Ви зареєструвалися')
            return render(request, 'blog/index.html', {'title': 'Мій блог'})
        else:
            errors_massage = ''
            for error in form.errors:
                errors_massage += f'Помилка: "{error}"'
            messages.error(request, errors_massage)
            return render(request, 'users/signup.html', {'form': form})


class LogInView:

    def authenticate(self, request, username=None, password=None):
        login_valid = settings.ADMIN_LOGIN == username
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = Users(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None

    def user_login(request):
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)

            if form.is_valid():
                user = form.get_user()
                login(request, user)

                messages.success(request, 'Ви увійшли успішно!')
                return render(request, 'blog/index.html', {'title': 'Мій блог'})
            else:
                messages.error(request, 'Invalid username or password')

        return render(request, 'users/login.html', {'form': UserLoginForm()})


class LogOutView:
    def user_logout(request):
        logout(request)
        messages.success(request, 'Ви вийшли успішно!')
        return redirect('login')


class UserProfileView:
    def user_profile(request):
        # logger.info(f"{request.user.username}")
        return render(request, 'users/profile.html')


class DeleteUserView(DeleteView):
    model = Users
    success_url = reverse_lazy('signup')

    def form_valid(self, form):
        messages.success(self.request, message='Ви успішно видалили ваш обліковий запис!')
        return super().form_valid(form)


class UpdateUserView(UpdateView):
    model = Users
    fields = ['username', 'pib', 'photo']
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, message='Ви успішно редагували ваш обліковий запис!')
        return super().form_valid(form)

def user_contact(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not authenticated! Please login first')
        return redirect('login')

    form = SendBackEmailForm()

    if request.method == 'POST':
        form = SendBackEmailForm(request.POST)

        if form.is_valid():
            try:
                email = EmailMessage(
                    subject=form.cleaned_data['subject'],
                    body=form.cleaned_data['message_content'],
                    from_email='dania.tenditnyi@demomailtrap.com',
                    to=['dania.tenditnyi@gmail.com']
                )
                email.send()

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

    return render(request, 'users/contact.html', {'form': form})
