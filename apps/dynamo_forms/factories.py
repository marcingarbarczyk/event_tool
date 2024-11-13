import factory
from factory import Iterator
from factory.django import DjangoModelFactory

from apps.dynamo_forms.models import Answer, Field, FieldChoice, Form, Section, UserAnswers


class FormFactory(DjangoModelFactory):
    class Meta:
        model = Form

    name = factory.Faker('name')


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    name = factory.Faker('name')
    form = Iterator(Form.active_objects.all())


class FieldFactory(DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Faker('word')
    label = factory.Faker('sentence')
    field_type = Field.TEXT
    section = Iterator(Section.active_objects.all())
    required = factory.Faker('boolean')


class FieldChoiceFactory(DjangoModelFactory):
    class Meta:
        model = FieldChoice

    field = Iterator(Field.active_objects.all())
    choice = factory.Faker('word')


class UserAnswersFactory(DjangoModelFactory):
    class Meta:
        model = UserAnswers


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    field = factory.SubFactory(FieldFactory)
    answer = factory.Faker('sentence')
    user_answers = factory.SubFactory(UserAnswersFactory)
