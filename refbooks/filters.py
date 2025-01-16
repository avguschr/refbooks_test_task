from django.db.models import QuerySet
from django_filters import rest_framework as filters

from refbooks.models import Refbook, RefbookElement, RefbookVersion


class RefbooksListFilter(filters.FilterSet):
    """
    Фильтр для получения справочников.
    """
    date = filters.CharFilter(method='date_filter')

    def date_filter(self, qs: QuerySet[Refbook], name: str, value: str) -> QuerySet[Refbook]:
        """
        Фильтр по дате.
        """
        refbooks_ids = RefbookVersion.objects.filter(start_date__date__lte=value).values('refbook_id')
        return qs.filter(id__in=refbooks_ids)

    class Meta:
        model = Refbook
        fields = ('date',)


class RefbookElementsListFilter(filters.FilterSet):
    """
    API для получения элементов справочника.
    """
    version = filters.CharFilter(method='version_filter', required=False)

    def version_filter(self, qs: QuerySet[RefbookElement], name: str, value: str) -> QuerySet[RefbookElement]:
        """
        Фильтр по версии справочника.
        """
        return qs.filter(refbook_version__version=value)

    class Meta:
        model = RefbookElement
        fields = ('refbook_version',)
