from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    private_fields = ['is_active', 'created_at', 'updated_at']

    def get_fields(self):
        fields = super().get_fields()
        required_fields = fields.copy()

        if not self.context['request'].user.is_superuser:

            for field in fields:
                if field in self.private_fields:
                    required_fields.pop(field)

        return required_fields
