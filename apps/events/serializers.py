from rest_framework import serializers

from apps.events.models import Registration


class NewRegistartionSerializers(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    form_id = serializers.CharField(max_length=255)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
