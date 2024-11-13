from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import ActiveMixin, Orderable, TimestampMixin


class Form(TimestampMixin, ActiveMixin):
    """
    Form model
    """

    name = models.CharField(
        max_length=200,
        verbose_name=_('name'),
    )

    def __str__(self):
        return f'Form #{self.id} {self.name}'

    class Meta:
        verbose_name = _('form')
        verbose_name_plural = _('forms')


class Section(Orderable, ActiveMixin):
    """
    Section model
    """

    name = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name=_('name'),
    )
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name=_('form'),
    )
    field_choice = models.ForeignKey(
        'FieldChoice',
        on_delete=models.SET_NULL,
        related_name='sections',
        null=True,
        blank=True,
        verbose_name=_('linked choice'),
    )

    def __str__(self):
        return f'Section #{self.id} {self.name}'

    class Meta(Orderable.Meta):
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Field(Orderable, ActiveMixin):
    """
    Field model
    """

    TEXT = 'text'
    RADIO = 'radio'
    FIELD_TYPE_CHOICES = [(TEXT, _('Text Field')), (RADIO, _('Select'))]

    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )
    label = models.CharField(
        max_length=100,
        verbose_name=_('label'),
    )
    field_type = models.CharField(
        max_length=15,
        choices=FIELD_TYPE_CHOICES,
        default=TEXT,
        verbose_name=_('type'),
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name=_('section'),
    )
    required = models.BooleanField(
        default=False,
        verbose_name=_('required'),
    )

    def __str__(self):
        return f'Form #{self.section.form.id} Section #{self.section.id} Field #{self.id} {self.name}'

    class Meta(Orderable.Meta):
        verbose_name = _('field')
        verbose_name_plural = _('fields')


class FieldChoice(Orderable, ActiveMixin):
    """
    FieldChoice model
    """

    field = models.ForeignKey(
        Field,
        related_name='choices',
        on_delete=models.CASCADE,
        verbose_name=_('field'),
    )
    choice = models.CharField(
        max_length=200,
        verbose_name=_('choice'),
    )

    def __str__(self):
        return f'Choice #{self.id} {self.choice}'

    class Meta(Orderable.Meta):
        verbose_name = _('field choice')
        verbose_name_plural = _('field choices')


class UserAnswers(TimestampMixin):
    """
    UserAnswers model
    """

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = _('user answers')
        verbose_name_plural = _('user answers')


class Answer(models.Model):
    """
    Answer model
    """

    field = models.ForeignKey(
        Field,
        on_delete=models.PROTECT,
        verbose_name=_('field'),
    )
    answer = models.CharField(
        max_length=200,
        verbose_name=_('answer'),
    )
    user_answers = models.ForeignKey(
        UserAnswers,
        related_name='answers',
        verbose_name=_('user answers'),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f'Answer #{self.id} {self.answer}'

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')
