from rest_framework.schemas.openapi import AutoSchema
from rest_framework import serializers
from rest_framework.fields import empty

class MetaDataSchema(AutoSchema):
    """Extension of ``AutoSchema`` to add support for custom field schemas."""

    def map_serializer(self, serializer):
        # Assuming we have a valid serializer instance.
        required = []
        properties = {}
        model = getattr(getattr(self.view, 'queryset', None), 'model', None)

        for field in serializer.fields.values():
            if isinstance(field, serializers.HiddenField):
                continue

            if field.required:
                required.append(field.field_name)

            schema = self.map_field(field)
            schema['fieldType'] = str(field).split("(")[0].replace("Field", "")

            if field.read_only:
                schema['readOnly'] = True
            if field.write_only:
                schema['writeOnly'] = True
            if field.allow_null:
                schema['nullable'] = True
            if field.default is not None and field.default != empty and not callable(field.default):
                schema['default'] = field.default
            if field.help_text:
                schema['description'] = str(field.help_text)
            if field.label:
                schema['label'] = field.label
            self.map_field_validators(field, schema)

            properties[field.field_name] = schema

        result = {
            'type': 'object',
            'properties': properties
        }
        if required:
            result['required'] = required

        return result