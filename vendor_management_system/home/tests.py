from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationTest(APITestCase):

    def test_registration_success(self):
        url = reverse('home:registration')
        data = {
            "username": "TestUser",
            "email": "example@gmail.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['status_message'], "Registration Successful.")

    def test_registration_failure(self):
        url = reverse('home:registration')
        invalid_data = {
            "username": "TestUser",
            "email": "example@gmail",
            "password": "testpassword"
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.data['status_code'], -1)
                

class LoginTest(APITestCase):

    def setUp(self):
        self.create_user(email="test@example.com", username="testuser", password="testpassword")

    def create_user(self, email, username, password):
        User.objects.create_user(email=email, username=username, password=password)

    def test_login_success(self):
        url = reverse('home:login')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['status_code'], 1)
        self.assertEqual(response.data['results']['user_details']['username'], 'testuser')
        self.assertEqual(response.data['results']['user_details']['email'], 'test@example.com')

    def test_login_failure(self):
        url = reverse('home:login')
        invalid_data = {
            "email": "example@gmail.com",
            "password": "testpassword"
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.data['status_code'], -1)
        self.assertEqual(response.data['status_message'], 'Please provide valid login credentials.')
        