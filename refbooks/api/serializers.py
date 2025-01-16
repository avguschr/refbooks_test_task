from rest_framework import serializers

from refbooks.models import Refbook, RefbookElement


class RefbookListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения справочников.
    """

    class Meta:
        fields = (
            'id',
            'title',
        )
        model = Refbook


class RefbookElementsListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения элементов справочника.
    """

    class Meta:
        fields = (
            'code',
            'value',
        )
        model = RefbookElement


class RefbookCheckElementParamsSerializer(serializers.Serializer):
    """
    Сериализатор для параметров запроса проверки наличия элемента в справочнике.
    """
    code = serializers.CharField(required=True)
    value = serializers.CharField(required=True)
    version = serializers.CharField(required=False)
