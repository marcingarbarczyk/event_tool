from django.contrib import admin

from .models import Answer, Field, FieldChoice, Form, Section, UserAnswers


class SectionInline(admin.TabularInline):
    model = Section


class FieldChoiceInline(admin.TabularInline):
    model = FieldChoice


class FieldInline(admin.TabularInline):
    model = Field


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [SectionInline]
    list_display = (
        'id',
        'name',
        'created_at',
        'updated_at',
        'is_active',
    )
    list_filter = ('is_active',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [FieldInline]
    list_display = (
        'id',
        'name',
        'form',
        'is_active',
    )
    list_filter = (
        'is_active',
        'form',
    )


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    inlines = [FieldChoiceInline]
    list_filter = (
        'is_active',
        'field_type',
    )
    list_display = (
        'id',
        'name',
        'label',
        'field_type',
        'section',
        'order',
        'is_active',
    )


@admin.register(FieldChoice)
class FieldChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'field',
        'choice',
        'is_active',
    )
    list_filter = (
        'is_active',
        'field',
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'field',
        'answer',
        'user_answers',
    )
    list_filter = (
        'user_answers',
        'field',
    )


@admin.register(UserAnswers)
class UserAnswersAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_filter = [
        'created_at',
    ]
    list_display = (
        'id',
        'created_at',
        'updated_at',
    )
