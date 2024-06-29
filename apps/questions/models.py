from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from apps.core.models import TimeStampedModel


class Tour(TimeStampedModel):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    start_time = models.DateTimeField(verbose_name=_('start time'))
    end_time = models.DateTimeField(verbose_name=_('end time'))
    count = models.PositiveIntegerField(default=0, verbose_name=_('count'))
    testing_time = models.TimeField(default=timedelta(hours=1), verbose_name=_('testing time'))

    class Meta:
        verbose_name = _('tour')
        verbose_name_plural = _('tours')

    def __str__(self):
        return f"{self.name}"


class Question(TimeStampedModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tour")
    text = models.TextField(verbose_name=_('Text'))
    photo = models.ImageField(upload_to='questions/', null=True, blank=True, verbose_name=_('photo'))
    correct_answer = models.CharField(max_length=200, verbose_name=_('correct answer'))
    incorrect_answer_1 = models.CharField(max_length=200, verbose_name=_('incorrect answer 1'))
    incorrect_answer_2 = models.CharField(max_length=200, verbose_name=_('incorrect answer 2'))
    incorrect_answer_3 = models.CharField(max_length=200, verbose_name=_('incorrect answer 3'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    # objects = MemberManager()

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/vendor/jquery/jquery.init.js',
            'admin/js/actions.js',
            'admin/js/vendor/jquery/ui/jquery.ui.widget.js',
            'admin/js/vendor/jquery/ui/jquery.ui.mouse.js',
            'admin/js/vendor/jquery/ui/jquery.ui.draggable.js',
            'admin/js/vendor/jquery/ui/jquery.ui.position.js',
            'admin/js/vendor/jquery/ui/jquery.ui.resizable.js',
            'admin/js/vendor/jquery/ui/jquery.ui.button.js',
            'admin/js/vendor/jquery/ui/jquery.ui.dialog.js',
            'admin/js/vendor/jquery/ui/jquery.ui.autocomplete.js',
        )
        css = {
            'all': (
                'admin/css/widgets.css',
            ),
        }

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return f"{self.text}"
