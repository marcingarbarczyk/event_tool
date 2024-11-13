from django import forms

from apps.dynamo_forms.models import Field, FieldChoice, Form, Section


class DynamoForm(forms.Form):
    FIELD_TYPE_TEXT = Field.TEXT
    FIELD_TYPE_SELECT = Field.RADIO

    def __init__(self, *args, **kwargs):
        self.form_id = kwargs.pop('form_id')
        self.form = Form.active_objects.active().get(id=self.form_id)
        self.sections = Section.active_objects.active().filter(form=self.form)
        self.ignore_fields = []
        super(DynamoForm, self).__init__(*args, **kwargs)
        self._initialize_form_fields()

    def _initialize_form_fields(self):
        for section in self.sections:
            self._set_section_fields(section)

    def _set_section_fields(self, section):
        fields = section.fields.all().filter(is_active=True)
        for field in fields:
            self._set_appropriate_field(field)

    def _set_appropriate_field(self, field):
        if field.field_type == self.FIELD_TYPE_TEXT:
            self.fields[f'{field.name}'] = forms.CharField(label=field.label, required=field.required, max_length=200)
        elif field.field_type == self.FIELD_TYPE_SELECT:
            choices = [(choice.id, choice.choice) for choice in FieldChoice.active_objects.active().filter(field=field)]
            self.fields[f'{field.name}'] = forms.ChoiceField(choices=choices, required=field.required)

    def _check_section_field_choice_valid(self, section):
        section_field_choice = section.field_choice
        if section_field_choice:
            field = section_field_choice.field
            try:
                user_choice = self.data[field.name]
            except KeyError:
                return False
            if int(user_choice) != section_field_choice.id:
                self._update_ignore_fields_and_remove_field(section)
        return True

    def _update_ignore_fields_and_remove_field(self, section):
        for field in section.fields.active():
            self.ignore_fields.append(field.name)
            del self.fields[f'{field.name}']

    def is_valid(self):
        return all(self._check_section_field_choice_valid(section) for section in self.sections) and super().is_valid()
