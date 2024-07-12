from django.test import TestCase
from apps.commons.models import Bank
from apps.commons.api.serializers import BankSerializer


class BankSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {"name": "Bank of Test"}
        self.invalid_data = {
            "name": "",
        }
        self.bank = Bank.objects.create(name="Old Bank")

    def test_serializer_with_valid_data(self):
        serializer = BankSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, self.valid_data)

    def test_serializer_with_invalid_data(self):
        serializer = BankSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_serializer_create(self):
        serializer = BankSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        bank = serializer.save()
        self.assertEqual(bank.name, self.valid_data["name"])

    def test_serializer_update(self):
        update_data = {"name": "New Bank"}
        serializer = BankSerializer(self.bank, data=update_data)
        self.assertTrue(serializer.is_valid())
        updated_bank = serializer.save()
        self.assertEqual(updated_bank.name, update_data["name"])

    def test_serializer_representation(self):
        serializer = BankSerializer(self.bank)
        data = serializer.data
        self.assertEqual(data["name"], self.bank.name)
