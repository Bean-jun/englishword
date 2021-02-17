from django.contrib import admin
from .models import WordTable
# Register your models here.


class WordTableManger(admin.ModelAdmin):
    list_display = ['word', 'trans', 'use_num']


admin.site.register(WordTable, WordTableManger)