from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import TelegramUser
from apps.questions.models import Tour, Question


class Testing(models.Model):
    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name=_("telegram user"))
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name=_("tour"))
    started_at = models.DateTimeField(verbose_name=_("started at"))
    finished_at = models.DateTimeField(verbose_name=_("finished at"))
    spent_time = models.TimeField(verbose_name=_("spent time"), default=timedelta(hours=1))
    is_active = models.BooleanField(verbose_name=_("active"), default=True)
    correct_answers_count = models.IntegerField(verbose_name=_("correct answers"), default=0)

    class Meta:
        verbose_name = _("testing")
        verbose_name_plural = _("testings")


class Answer(models.Model):
    ANSWER_CHOICES = (
        (_('correct_answer'), _('Correct Answer')),
        (_('incorrect_answer_1'), _("incorrect Answer 1")),
        (_('incorrect_answer_2'), _("incorrect Answer 2")),
        (_('incorrect_answer_3'), _("incorrect Answer 3")),
    )

    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name=_("telegram user"))
    testing = models.ForeignKey(Testing, on_delete=models.CASCADE, verbose_name=_("testing"))
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name=_("tour"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"))
    received_answer = models.CharField(max_length=200, verbose_name=_("received answer"))
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")

    def __str__(self):
        return f"{self.tg_user}"
