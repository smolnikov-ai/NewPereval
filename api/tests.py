from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import *
from api.serializers import PerevalSerializer


class PerevalTestCase(APITestCase):
    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            user=User.objects.create(email='pereval_1@example.com', fam='pereval_1_fam', name='pereval_1_name',
                                     otc='pereval_1_otc', phone=111111111111,),
            coords=Coords.objects.create(latitude=11.1111, longitude=11.1111, height=1111,),
            level=Level.objects.create(winter="1А", summer="1А", autumn="1А", spring="1А",),
            beauty_title='pereval_1_beauty_title',
            title='pereval_1_title',
            other_titles='pereval_1_other_titles',
            connect='pereval_1_connect',
            add_time='2001-01-11T01:11:11.111111Z',
            status="new",
        )

        self.pereval_2 = Pereval.objects.create(
            user=User.objects.create(email='pereval_2@example.com', fam='pereval_2_fam', name='pereval_2_name',
                                     otc='pereval_2_otc', phone=222222222222,),
            coords=Coords.objects.create(latitude=22.2222, longitude=22.2222, height=2222,),
            level=Level.objects.create(winter="2А", summer="2А", autumn="2А", spring="2А",),
            beauty_title='pereval_2_beauty_title',
            title='pereval_2_title',
            other_titles='pereval_2_other_titles',
            connect='pereval_2_connect',
            add_time='2002-02-02 02:22:22',
            status="rejected",
        )

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class PerevalSerialiserTestCase(TestCase):

    def setUp(self):
        self.valid_pereval_data = {
            'user': {
                'email': 'test@example.com',
                'fam': 'Иванов',
                'name': 'Иван',
                'otc': 'Иванович',
                'phone': '123456789012'
            },
            'coords': {
                'latitude': '55.123456',
                'longitude': '37.123456',
                'height': 1000
            },
            'level': {
                'winter': '1А',
                'summer': '1А',
                'autumn': '1А',
                'spring': '1А'
            },
            'beauty_title': 'Красивый перевал',
            'title': 'Тестовый перевал',
            'other_titles': 'Другие названия',
            'connect': 'Связь',
            'images': [
                {
                    'data': 'https://example.com/image1.jpg',
                    'title': 'Изображение 1'
                },
                {
                    'data': 'https://example.com/image2.jpg',
                    'title': 'Изображение 2'
                }
            ]
        }

    def test_pereval_serializer_valid_data(self):
        """Тест сериализатора перевала с валидными данными"""
        serializer = PerevalSerializer(data=self.valid_pereval_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        pereval = serializer.save()

        # Проверяем создание связанных объектов
        self.assertEqual(pereval.user.email, 'test@example.com')
        self.assertEqual(pereval.coords.latitude, Decimal('55.123456'))
        self.assertEqual(pereval.level.winter, '1А')
        self.assertEqual(pereval.images.count(), 2)

    def test_pereval_serializer_read_only_status(self):
        """Тест read-only поля status"""
        data = self.valid_pereval_data.copy()
        data['status'] = 'accepted'  # Попытка установить статус

        serializer = PerevalSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        pereval = serializer.save()

        # Статус должен быть по умолчанию, не 'accepted'
        self.assertEqual(pereval.status, 'new')

    def test_pereval_serializer_missing_required_fields(self):
        """Тест сериализатора перевала с отсутствующими обязательными полями"""
        incomplete_data = {
            'user': {
                'email': 'test@example.com',
                'fam': 'Иванов',
                'name': 'Иван'
            }
        }
        serializer = PerevalSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())

    def test_pereval_serializer_serialization(self):
        """Тест сериализации перевала в JSON"""
        # Создаем тестовые данные
        user = User.objects.create(
            email='test@example.com',
            fam='Иванов',
            name='Иван',
            phone='123456789012'
        )
        coords = Coords.objects.create(
            latitude=Decimal('55.123456'),
            longitude=Decimal('37.123456'),
            height=1000
        )
        level = Level.objects.create(
            winter='1А',
            summer='2А'
        )
        pereval = Pereval.objects.create(
            user=user,
            coords=coords,
            level=level,
            title='Тестовый перевал'
        )
        Images.objects.create(
            data='https://example.com/image.jpg',
            title='Тестовое изображение',
            pereval=pereval
        )

        serializer = PerevalSerializer(pereval)
        data = serializer.data

        # Проверяем структуру данных
        self.assertIn('user', data)
        self.assertIn('coords', data)
        self.assertIn('level', data)
        self.assertIn('images', data)
        self.assertEqual(data['title'], pereval.title)
        self.assertEqual(data['status'], pereval.status)

    def test_pereval_serializer_nested_objects(self):
        """Тест вложенных объектов в сериализаторе перевала"""
        serializer = PerevalSerializer(data=self.valid_pereval_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        # Проверяем, что вложенные сериализаторы работают корректно
        user_data = serializer.validated_data['user']
        coords_data = serializer.validated_data['coords']
        level_data = serializer.validated_data['level']

        self.assertEqual(user_data['email'], 'test@example.com')
        self.assertEqual(coords_data['latitude'], Decimal('55.123456'))
        self.assertEqual(level_data['winter'], '1А')

    def test_pereval_serializer_get_or_create_user(self):
        """Тест повторного использования пользователя через get_or_create"""
        # Создаем первый перевал
        serializer1 = PerevalSerializer(data=self.valid_pereval_data)
        self.assertTrue(serializer1.is_valid())
        pereval1 = serializer1.save()

        # Создаем второй перевал с тем же пользователем
        serializer2 = PerevalSerializer(data=self.valid_pereval_data)
        self.assertTrue(serializer2.is_valid())
        pereval2 = serializer2.save()

        # Проверяем, что пользователь один и тот же
        self.assertEqual(pereval1.user, pereval2.user)
        self.assertEqual(User.objects.count(), 1)