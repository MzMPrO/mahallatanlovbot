from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from django import forms

from apps.questions.models import Tour, Question


class TourAdminForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'


class QuestionInline(ImportExportMixin, admin.StackedInline):
    model = Question
    extra = 1


# class TestingInline(admin.TabularInline):
#     model = Testing
#     extra = 1

# def get_queryset(self, request):
#     fields = super().get_queryset(request)
#     return fields.order_by('-correct_answers_count')
#
# fieldsets = [
#     (None, {
#         'fields': [
#             'member',
#             'correct_answers_count',
#             'spent_time'
#         ],
#     }),
# ]
#
# def has_add_permission(self, request, obj):
#     return False
#
# def has_delete_permission(self, request, obj=None):
#     return False
#
# def has_change_permission(self, request, obj=None):
#     return False


class TourAdmin(ImportExportModelAdmin):
    form = TourAdminForm

    list_display = ('name', 'start_time', 'end_time', 'count', 'testing_time', 'created_at', 'id')
    list_filter = ['start_time', 'end_time']
    search_fields = ('name',)

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', "count", "testing_time", 'start_time', 'end_time'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.updated_at = timezone.now()
            instance.save()
        formset.save_m2m()


class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('text', 'tour', 'is_active', 'created_at')
    list_filter = ('tour', 'is_active', 'created_at')
    search_fields = ('text', 'tour__name',)

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('text', 'tour', 'photo'),
        }),
        (_('Answers'), {
            'fields': ('correct_answer',
                       'incorrect_answer_1',
                       'incorrect_answer_2',
                       'incorrect_answer_3'
                       ),
        }),
        (_('Status'), {
            'fields': ('is_active',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)


admin.site.register(Tour, TourAdmin)
admin.site.register(Question, QuestionAdmin)
