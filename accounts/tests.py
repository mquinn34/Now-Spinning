from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserFieldTest(TestCase):
    def test_custom_fields(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            display_name="Test User",
            bio="Loves vinyl records and coffee."
        )

        self.assertEqual(user.display_name, "Test User")
        self.assertEqual(user.bio, "Loves vinyl records and coffee.")
        self.assertFalse(user.avatar) 


class SimpleUserTests(TestCase):
    def test_create_user(self):
        """A user can be created with username and password."""
        user = User.objects.create_user(username="testuser", password="pass1234")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("pass1234"))

    def test_string_representation(self):
        """The string representation should be the username."""
        user = User.objects.create_user(username="stringtest", password="pass1234")
        self.assertEqual(str(user), "stringtest")
