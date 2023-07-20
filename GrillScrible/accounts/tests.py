from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import *

# Create your tests here.

class RegisterTestCase(APITestCase):
    '''Class to test profile registration'''
    def test_register(self):
        data={
            'username':'testcase',
            'email':'testcase@examples.com',
            'password':'Password@123',
            'password2':'Password@123'
        }
        response=self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        
class LoginLogoutTestCase(APITestCase):
    '''Class to test login, logout and refresh functionality'''
    def setUp(self):
        # Method for setting up the test fixture before exercising it.
        self.user=get_user_model().objects.create_user(username='newtestcase',email='newtestcase@examples.com',password='NewPassword@123')
        
    def test_login_logout(self):
        data={
            'username':'newtestcase',
            'email':'newtestcase@examples.com',
            'password':'NewPassword@123'
        }
        # Try to login to a user with field is_active=False
        self.user.is_active=False
        self.user.save()
        response= self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        # Changing field is_active=True so we can in active state
        self.user.is_active=True
        self.user.save()
        response= self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # Ideal value of respose.data={'username': 'newtestcase', 'tokens': {'refresh': '....', 'access': '....'}}
        self.assertTrue('tokens' in response.data)
        
        # Check refresh functionality by paaing refresh token from previos response
        token=response.data['tokens'] 
        response=self.client.post(reverse('token_refresh'),{'refresh':token['refresh']})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        # Modify refresh token and test should fail
        response=self.client.post(reverse('token_refresh'),refresh_token={'refresh':'abcd'})
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        # Testing logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {token["access"]}')
        response=self.client.post(reverse('logout'),data=token)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        

class ProfileTestCase(APITestCase):
    
    def setUp(self):
        # Method for setting up the test fixture before exercising it.
        self.user=get_user_model().objects.create_user(username='testcase',email='newtestcase@examples.com',password='Password@123')
        
    def test_profile_get(self):
        self.client.force_authenticate(user=self.user)
        response=self.client.get(reverse('profile_detail'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['username'],self.user.username)
        self.assertEqual(response.data['email'],self.user.email)
        self.assertEqual(response.data['first_name'],self.user.first_name)
        self.assertEqual(response.data['last_name'],self.user.last_name)
        self.assertEqual(response.data['date_joined'],self.user.date_joined.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    
    def test_profile_put(self):
        self.client.force_authenticate(user=self.user)
        data={
            "first_name": "test",
            "last_name": "testing",
            "email": "test@xyz.com",
            "bio": "I am the test profile"
        }
        response=self.client.put(reverse('profile_detail'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # Checking the response data against the data sent to certify the update
        self.assertEqual(response.data['username'],self.user.username)
        self.assertEqual(response.data['email'],self.user.email)
        self.assertEqual(response.data['first_name'],self.user.first_name)
        self.assertEqual(response.data['last_name'],self.user.last_name)
        self.assertEqual(response.data['date_joined'],self.user.date_joined.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))