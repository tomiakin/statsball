from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """Base serializer adding success wrapper"""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if isinstance(data, list):
            return {
                'status': 'success',
                'data': data,
                'message': None
            }
        return data


class HalModelSerializer(BaseSerializer):
    """Base serializer that adds HAL-style _links"""
    _links = serializers.SerializerMethodField('get__links')

    def get__links(self, obj):
        """Default empty implementation"""
        return {}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        links = self.get__links(instance)
        if links:
            data['_links'] = links
        return data
