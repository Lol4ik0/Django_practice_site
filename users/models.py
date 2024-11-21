from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    GENDERS = (
        ('m', 'male'),
        ('f', 'female')
    )

    pib         = models.CharField(max_length=30, verbose_name="ПІБ")
    birth_date  = models.DateField(verbose_name="Дата народження", db_index=True, default='2000-09-12')
    gender      = models.CharField(max_length=1, verbose_name='Стать', choices=GENDERS, default='m')
    email       = models.EmailField(verbose_name="Пошта", db_index=True)
    photo       = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    phone       = models.CharField(max_length=10, verbose_name="Номер телефону", default="")

    def get_absolute_url_for_update(self):
        return reverse('update_user', kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse('delete_user', kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.first_name} {self.last_name}, email: {self.birth_date}, password: {self.password}'

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
        ordering = ['-birth_date', 'pib']
