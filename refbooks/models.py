from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Refbook(models.Model):
    """
    Модель для справочника.
    """

    code = models.CharField(
        verbose_name="Код", max_length=100, blank=False, null=False, unique=True
    )
    title = models.CharField(
        verbose_name="Наименование", max_length=300, blank=False, null=False
    )
    description = models.TextField(verbose_name="Описание", blank=True, default="")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"


class RefbookVersion(models.Model):
    """
    Модель для версии справочника.
    """

    refbook = models.ForeignKey(
        to=Refbook,
        blank=False,
        null=False,
        related_name="refbooks",
        on_delete=models.CASCADE,
        verbose_name="Справочник"
    )
    version = models.CharField(
        verbose_name="Версия", max_length=50, blank=False, null=False
    )
    start_date = models.DateTimeField(
        verbose_name="Дата начала действия версии", default=timezone.now
    )

    def validate_unique(self, exclude=None):
        qs = RefbookVersion.objects.filter(refbook=self.refbook)
        if qs.filter(start_date=self.start_date).exists():
            raise ValidationError(
                "В данном справочнике уже есть версия с такой датой начала действия."
            )
        if qs.filter(version=self.version).exists():
            raise ValidationError("В данном справочнике уже есть такая версия.")

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(RefbookVersion, self).save(*args, **kwargs)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"


class RefbookElement(models.Model):
    """
    Модель для элемента версии справочника.
    """

    refbook_version = models.ForeignKey(
        to=RefbookVersion,
        blank=False,
        null=False,
        related_name="refbooks_versions",
        on_delete=models.CASCADE,
        verbose_name="Версия справочника"
    )
    code = models.CharField(
        verbose_name="Код элемента", max_length=100, blank=False, null=False
    )
    value = models.CharField(
        verbose_name="Значение элемента", max_length=300, blank=False, null=False
    )

    def __str__(self):
        return self.code

    def validate_unique(self, exclude=None):
        qs = RefbookElement.objects.filter(
            refbook_version=self.refbook_version, code=self.code
        )
        if qs.exists():
            raise ValidationError(
                "В данной версии справочника уже есть элемент с таким кодом."
            )

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(RefbookElement, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Элемент версии справочника"
        verbose_name_plural = "Элементы версий справочников"
