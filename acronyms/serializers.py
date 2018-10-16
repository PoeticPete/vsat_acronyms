from rest_framework import serializers
from acronyms.models import Acronym
from django.contrib.auth.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class AcronymSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):

    class Meta:
        model = Acronym
        fields = ('id', 'acronym', 'description', 'definition', 'created', )
        depth = 1
