from typing import Any

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from refbooks.api.serializers import (RefbookCheckElementParamsSerializer,
                                      RefbookElementsListSerializer,
                                      RefbookListSerializer)
from refbooks.filters import RefbookElementsListFilter, RefbooksListFilter
from refbooks.models import Refbook, RefbookElement
from refbooks.utils import get_current_refbook_version


class RefbooksListAPIView(ListAPIView):
    """
    API для получения списка справочников.
    """
    model = Refbook
    queryset = Refbook.objects.all()
    serializer_class = RefbookListSerializer
    filterset_class = RefbooksListFilter


class RefbookElementsListAPIView(ListAPIView):
    """
    API для получения элементов справочника.
    """
    model = RefbookElement
    queryset = RefbookElement.objects.all()
    serializer_class = RefbookElementsListSerializer
    filterset_class = RefbookElementsListFilter

    def get_queryset(self) -> QuerySet[RefbookElement]:
        version = self.request.query_params.get('version', None)

        refbook = Refbook.objects.filter(id=self.kwargs['id']).first()

        qs = super().get_queryset()

        if not version:
            current_version = get_current_refbook_version(refbook)
            qs = qs.filter(refbook_version_id=current_version)

        return qs


class RefbookCheckElementAPIView(APIView):
    """
    API для проверки наличия элемента в справочнике.
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        params_serializer = RefbookCheckElementParamsSerializer(data=request.query_params)
        params_serializer.is_valid(raise_exception=True)
        refbook = Refbook.objects.filter(id=self.kwargs['id']).first()
        code = params_serializer.validated_data['code']
        value = params_serializer.validated_data['value']
        version = params_serializer.validated_data.get('version', None)

        if not version:
            version = get_current_refbook_version(refbook)

        element = RefbookElement.objects.filter(code=code, value=value, refbook_version__version=version,
                                                refbook_version__refbook_id=refbook).first()
        if not element:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
