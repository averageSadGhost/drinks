from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from drinks.models import Drink

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.drink = Drink.objects.create(name='Test Drink', description='Test Description', author_id=self.user)

    def get_auth_token(self, username, password):
        url = reverse('login')
        response = self.client.post(url, {'username': username, 'password': password}, format='json')
        return response.data['access']

    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_user_by_id(self):
        url = reverse('get_user_by_id', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_get_all_users_as_admin(self):
        token = self.get_auth_token('admin', 'adminpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('get_all_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count())

    def test_get_all_users_as_non_admin(self):
        token = self.get_auth_token('testuser', 'testpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('get_all_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_drink_as_authenticated_user(self):
        token = self.get_auth_token('testuser', 'testpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('drink_list')
        data = {'name': 'New Drink', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Drink.objects.filter(name='New Drink').exists())


    def test_create_drink_as_unauthenticated_user(self):
        url = reverse('drink_list')
        data = {'name': 'New Drink', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_drink_as_author(self):
        token = self.get_auth_token('testuser', 'testpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('drink_detail', args=[self.drink.id])
        data = {'name': 'Updated Drink', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.drink.refresh_from_db()
        self.assertEqual(self.drink.name, 'Updated Drink')

    def test_update_drink_as_non_author(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        token = self.get_auth_token('otheruser', 'otherpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('drink_detail', args=[self.drink.id])
        data = {'name': 'Updated Drink', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_drink_as_admin(self):
        token = self.get_auth_token('admin', 'adminpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('drink_detail', args=[self.drink.id])
        data = {'name': 'Updated Drink', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.drink.refresh_from_db()
        self.assertEqual(self.drink.name, 'Updated Drink')

    def test_delete_drink_as_author(self):
        token = self.get_auth_token('testuser', 'testpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('drink_detail', args=[self.drink.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Drink.objects.filter(id=self.drink.id).exists())

    def test_delete_drink_as_non_author(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        token = self.get_auth_token('otheruser', 'otherpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('drink_detail', args=[self.drink.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_drink_as_admin(self):
        token = self.get_auth_token('admin', 'adminpass')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('drink_detail', args=[self.drink.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Drink.objects.filter(id=self.drink.id).exists())
