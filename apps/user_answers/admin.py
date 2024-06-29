from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .models import Testing, Answer


class TimeFormatWidget(forms.TimeInput):
    def format_value(self, value):
        return value.strftime('%H:%M:%S') if value else ''


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    exclude = ('tour', 'tg_user')

    def has_add_permission(self, request, obj=None):
        return False


class TestingAdmin(admin.ModelAdmin):
    list_display = ('id', 'tg_user', 'tour', 'started_at', 'finished_at', 'spent_time_formatted',
                    'correct_answers_count')
    formfield_overrides = {
        models.TimeField: {'widget': TimeFormatWidget},
    }

    def spent_time_formatted(self, obj):
        return obj.spent_time.strftime('%H:%M:%S') if obj.spent_time else ''

    spent_time_formatted.short_description = _('Spent Time')

    search_fields = ['tg_user__username',
                     'tour__name', "tg_user__chat_id", 'tg_user__name']
    list_filter = ['tour']
    fieldsets = (
        (None, {
            'fields': ('tg_user', 'tour', 'started_at', 'finished_at', 'spent_time', 'correct_answers_count')
        }),
    )
    inlines = [AnswerInline]

    def has_add_permission(self, request):
        return False


# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('tg_user', 'testing', 'tour', 'question', 'received_answer', 'created_at', 'updated_at')
#     search_fields = ['tg_user__username', 'tour__name',
#                      'question__text']
#     fieldsets = (
#         (None, {
#             'fields': ('tg_user', 'testing', 'tour', 'question', 'received_answer')
#         }),
#     )
#

admin.site.register(Testing, TestingAdmin)
# admin.site.register(Answer, AnswerAdmin)
