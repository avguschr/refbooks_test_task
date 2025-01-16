import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from refbooks.factories import (RefbookElementFactory, RefbookFactory,
                                RefbookVersionFactory)


class RegionsAPITestCase(APITestCase):
    """
    Тест-кейс для API справочников.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.refbook_1 = RefbookFactory()
        cls.refbook_2 = RefbookFactory()
        cls.refbook_3 = RefbookFactory()
        cls.version_1_1 = RefbookVersionFactory(refbook=cls.refbook_1, start_date=datetime.datetime(2025, 1, 1))
        cls.version_1_2 = RefbookVersionFactory(refbook=cls.refbook_1, start_date=datetime.datetime(2024, 12, 15))
        cls.version_1_3 = RefbookVersionFactory(refbook=cls.refbook_1,
                                                start_date=datetime.datetime.now() + datetime.timedelta(days=2))
        cls.version_2_1 = RefbookVersionFactory(refbook=cls.refbook_2, start_date=datetime.datetime(2025, 1, 5))
        cls.version_3_1 = RefbookVersionFactory(refbook=cls.refbook_3, start_date=datetime.datetime(2027, 1, 10))
        cls.element_1_1 = RefbookElementFactory(refbook_version=cls.version_1_1, code='1', value='Хирург')
        cls.element_1_2 = RefbookElementFactory(refbook_version=cls.version_1_1, code='2', value='Травматолог')
        cls.element_2_1 = RefbookElementFactory(refbook_version=cls.version_2_1)

    def test_get_all_refbooks(self) -> None:
        """Проверяет получение всех справочников."""
        response = self.client.get('/refbooks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_refbooks_with_date_filter(self) -> None:
        """Проверяет получение только тех справочников,
        у которых дата начала действия версии раннее или равна указанной."""
        date = '2025-01-05'
        response = self.client.get(f'/refbooks/?date={date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_refbook_elements_current_version(self) -> None:
        """Проверяет получение элементов текущей версии, если версия не указана."""
        id = self.refbook_1.id
        response = self.client.get(f'/refbooks/{id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_refbook_elements_specified_version(self) -> None:
        """Проверяет получение элементов текущей версии, если версия указана."""
        id = self.refbook_1.id
        version = self.version_2_1.version
        response = self.client.get(f'/refbooks/{id}/?version={version}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {'code': self.element_2_1.code, 'value': self.element_2_1.value})

    def test_refbook_element_current_version_exists(self) -> None:
        """Проверяет наличие элемента в справочнике текущей версии."""
        id = self.refbook_1.id
        code = '1'
        value = 'Хирург'
        response = self.client.get(f'/refbooks/{id}/check_element/?code={code}&value={value}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refbook_element_specified_version_exists(self) -> None:
        """Проверяет наличие элемента в справочнике указанной версии."""
        id = self.refbook_1.id
        code = '2'
        value = 'Травматолог'
        version = self.version_1_1.version
        response = self.client.get(f'/refbooks/{id}/check_element/?code={code}&value={value}&version={version}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refbook_element_required_params(self) -> None:
        """Проверяет, что параметры code и value обязательны при проверке наличия справочника."""
        id = self.refbook_1.id
        response = self.client.get(f'/refbooks/{id}/check_element/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
