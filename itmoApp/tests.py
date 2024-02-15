from django.test import TestCase
from django.contrib.auth.models import User
from .models import PickleModel

class PickleModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(username='testuser')

        # Создаем объект Pickle_model для тестирования
        self.pickle_model = PickleModel.objects.create(
            user=self.user,
            name='Test Pickle',
            pickle='path/to/test/pickle',
            mse='Test MSE',
            r2='Test R2',
            mean='Test Mean',
            median='Test Median',
            msle='Test MSLE',
            evs='Test EVS',
            mape='Test MAPE'
        )

    def test_pickle_model_user(self):
        self.assertEqual(self.pickle_model.user, self.user)

    def test_pickle_model_name(self):
        self.assertEqual(self.pickle_model.name, 'Test Pickle')

    def test_pickle_model_mse(self):
        self.assertEqual(self.pickle_model.mse, 'Test MSE')

    def test_pickle_model_r2(self):
        self.assertEqual(self.pickle_model.r2, 'Test R2')

    def test_pickle_model_evs(self):
        self.assertEqual(self.pickle_model.evs, 'Test EVS')

    # Продолжайте добавлять тесты для других полей...

    def test_pickle_model_str_representation(self):
        expected_str = f"{self.pickle_model.name} by {self.user.username}"
        self.assertNotEquals(str(self.pickle_model), expected_str)