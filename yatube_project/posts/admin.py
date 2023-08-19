from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
    # Позволяет менять/добавлять текст прям в таблице через интерфейс
    list_editable = ('group',)
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('pub_date',)
    # Это свойство сработает для всех колонок: где пусто — там будет эта строка
    empty_value_display = '-пусто-'


'''
При регистрации модели Post источником конфигурации для неё назначаем
класс PostAdmin
'''
admin.site.register(Post, PostAdmin)

'Регистрация даст возможность создавать новые группы через админ-зону.'
admin.site.register(Group)
