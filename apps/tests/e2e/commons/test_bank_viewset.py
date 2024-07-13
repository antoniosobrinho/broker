from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.clients.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.commons.models import Bank


class BankViewSetTest(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create some Bank instances
        Bank.objects.all().delete()

        self.bank1 = Bank.objects.create(name="Bank One")
        self.bank2 = Bank.objects.create(
            name="Bank Two",
        )

        # Create a JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_list_banks_authenticated(self):
        url = reverse("bank-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], self.bank1.name)
        self.assertEqual(response.data[1]["name"], self.bank2.name)

    def test_list_banks_unauthenticated(self):
        url = reverse("bank-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_bank_authenticated(self):
        url = reverse("bank-detail", args=[self.bank1.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.bank1.name)

    def test_retrieve_bank_unauthenticated(self):
        url = reverse("bank-detail", args=[self.bank1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
