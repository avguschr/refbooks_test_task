import factory.fuzzy

from refbooks.models import Refbook, RefbookElement, RefbookVersion


class RefbookFactory(factory.django.DjangoModelFactory):
    """Фабрика для справочников."""
    code = factory.fuzzy.FuzzyText(length=2)
    title = factory.fuzzy.FuzzyText(length=20)

    class Meta:
        model = Refbook


class RefbookVersionFactory(factory.django.DjangoModelFactory):
    """Фабрика для версий справочников."""
    refbook = factory.SubFactory(RefbookFactory, )
    version = factory.fuzzy.FuzzyText(length=2)
    start_date = factory.Faker('date_object')

    class Meta:
        model = RefbookVersion


class RefbookElementFactory(factory.django.DjangoModelFactory):
    """Фабрика для элементов справочников."""
    refbook_version = factory.SubFactory(RefbookVersionFactory)
    code = factory.fuzzy.FuzzyText(length=2)
    value = factory.fuzzy.FuzzyText(length=2)

    class Meta:
        model = RefbookElement
