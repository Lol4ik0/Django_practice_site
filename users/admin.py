from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Users
from users.forms import UserCreationForm, UserChangeForm


@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    model = Users
    # add_form = UserCreationForm
    # form = UserChangeForm

    list_display = ['username', 'pib', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'phone', 'photo']           # Поля которые отображаються
    list_display_links = ('username', 'pib', 'photo')                                               # Поля по которым можно нажать чтобы перейти в подробности
    search_fields = ('username', 'pib', 'email')                                                    # Поля по которым будет происходить поиск
    # list_editable = ('username', 'gender', 'phone', 'photo')                                      # Поля которые можно будет редактировать прямо из списка
    list_filter = ('pib', 'birth_date')                                                             # Поля которые можно будет фильтровать прямо в списке


    # Add user
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Детальна інформація',
            {
                'fields': (
                    'username',
                    'pib',
                    'email',
                    'gender',
                    'birth_date',
                    'phone',
                    'photo',
                )
            }
        )
    )

    # Edit user
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Детальна інформація',
            {
                'fields': (
                    # 'username',
                    'pib',
                    # 'email',
                    'gender',
                    'birth_date',
                    'phone',
                    'photo',
                )
            }
        )
    )

    # admin.site.register(Users, UserAdmin)
