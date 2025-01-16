from datetime import datetime

from refbooks.models import RefbookVersion


def get_current_refbook_version(refbook_id: int) -> RefbookVersion:
    """
    Возвращает текущую версию справочника.
    """
    return RefbookVersion.objects.filter(start_date__lt=datetime.now(), refbook_id=refbook_id).order_by('start_date').last()