import unittest
from unittest.mock import patch
from main import app

class TestLoginEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.valid_email = "test@example.com"
        self.valid_password = "password123"
        self.hashed_password = "hashed_password"
        self.user_record = {
            "email": self.valid_email,
            "password": self.hashed_password,
            "name": "Test User"
        }

    @patch("main.helpers.check_password")
    @patch("main.users.find_one")
    def test_login_success(self, mock_find_one, mock_check_password):
        # Mock database and password check
        mock_find_one.return_value = self.user_record
        mock_check_password.return_value = True

        response = self.client.post("/login", json={
            "email": self.valid_email,
            "password": self.valid_password
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
        self.assertEqual(response.json["email"], self.valid_email)

    @patch("main.users.find_one")
    def test_login_missing_fields(self):
        response = self.client.post("/login", json={
            "email": self.valid_email
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Email and password required")

    @patch("main.helpers.check_password")
    @patch("main.users.find_one")
    def test_login_incorrect_credentials(self, mock_find_one, mock_check_password):
        # Mock database and password check
        mock_find_one.return_value = self.user_record
        mock_check_password.return_value = False

        response = self.client.post("/login", json={
            "email": self.valid_email,
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["error"], "Incorrect user credentials")

if __name__ == "__main__":
    unittest.main()