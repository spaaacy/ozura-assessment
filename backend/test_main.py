import unittest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
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

class TestRegisterEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.url = "/register"

    @patch("main.users.find_one")
    @patch("main.users.insert_one")
    @patch("main.helpers.get_hashed_password")
    def test_register_success(self, mock_get_hashed_password, mock_insert_one, mock_find_one):
        # Mock behavior
        mock_find_one.return_value = None  # User does not exist
        mock_get_hashed_password.return_value = "hashed_password"
        
        # Request payload
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
        
        # Make POST request
        response = self.client.post(self.url, json=payload)
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "User registration successful")
        mock_insert_one.assert_called_once_with({
            "email": "john@example.com",
            "password": "hashed_password",
            "name": "John Doe"
        })

    @patch("main.users.find_one")
    def test_register_missing_fields(self, mock_find_one):
        # Mock behavior
        mock_find_one.return_value = None  # User does not exist

        # Missing email
        payload = {
            "name": "John Doe",
            "password": "password123"
        }
        response = self.client.post(self.url, json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Email and password required")

        # Missing password
        payload = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        response = self.client.post(self.url, json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Email and password required")

    @patch("main.users.find_one")
    def test_register_duplicate_user(self, mock_find_one):
        # Mock behavior
        mock_find_one.return_value = {"email": "john@example.com"}  # User exists

        # Request payload
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
        
        # Make POST request
        response = self.client.post(self.url, json=payload)
        
        # Assertions
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json["error"], "User already exists")

class TestTokenizeEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.url = "/tokenize"
        token = create_access_token(identity="user@example.com")
        self.headers = {"Authorization": f"Bearer {token}"}

    @patch("main.get_jwt_identity")
    @patch("main.tokens.insert_one")
    @patch("main.cipher.encrypt")
    def test_tokenize_success(self, mock_encrypt, mock_insert_one, mock_get_jwt_identity):
        # Mock behavior
        mock_get_jwt_identity.return_value = "user@example.com"
        mock_encrypt.return_value = b"encrypted_data"
        
        # Request payload
        payload = {
            "card_number": "4111111111111111",
            "name": "John Doe",
            "expiry": "12/25",
            "cvv": "123"
        }
        
        # Make POST request
        response = self.client.post(self.url, json=payload, headers=self.headers)
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json)
        mock_insert_one.assert_called_once()

    @patch("main.get_jwt_identity")
    def test_tokenize_missing_fields(self, mock_get_jwt_identity):
        # Mock behavior
        mock_get_jwt_identity.return_value = "user@example.com"
        
        # Missing card_number
        payload = {
            "name": "John Doe",
            "expiry": "12/25",
            "cvv": "123"
        }
        response = self.client.post(self.url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing card details")

        # Missing expiry
        payload = {
            "card_number": "4111111111111111",
            "name": "John Doe",
            "cvv": "123"
        }
        response = self.client.post(self.url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing card details")

    def test_tokenize_unauthorized(self):
        # Request payload
        payload = {
            "card_number": "4111111111111111",
            "name": "John Doe",
            "expiry": "12/25",
            "cvv": "123"
        }
        
        # Make POST request without Authorization header
        response = self.client.post(self.url, json=payload)
        
        # Assertions
        self.assertEqual(response.status_code, 401)
        self.assertIn("msg", response.json)
        self.assertEqual(response.json["msg"], "Missing Authorization Header")

class TestDetokenizeEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.url = "/detokenize"
        token = create_access_token(identity="user@example.com")
        self.headers = {"Authorization": f"Bearer {token}"}

    def tearDown(self):
        self.app_context.pop()

    @patch("main.get_jwt_identity")
    @patch("main.tokens.find_one")
    @patch("main.cipher.decrypt")
    def test_detokenize_success(self, mock_decrypt, mock_find_one, mock_get_jwt_identity):
        # Mock behavior
        mock_get_jwt_identity.return_value = "user@example.com"
        mock_find_one.return_value = {"encrypted_data": "encrypted_data", "user_email": "user@example.com"}
        mock_decrypt.return_value = b"4111111111111111|12/25|123|John Doe"
        
        # Request payload
        payload = {
            "token": "encrypted_data"
        }
        
        # Make POST request
        response = self.client.post(self.url, json=payload, headers=self.headers)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("card_details", response.json)
        self.assertEqual(response.json["card_details"], {'card_number': '4111111111111111', 'cvv': '123', 'expiry_date': '12/25', 'name': 'John Doe'})
        mock_find_one.assert_called_once_with({"token": "encrypted_data"})

    def test_detokenize_missing_fields(self):
        # Request payload with missing token
        payload = {}
        
        # Make POST request
        response = self.client.post(self.url, json=payload, headers=self.headers)
        
        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing token")

    def test_detokenize_unauthorized(self):
        # Request payload
        payload = {
            "token": "encrypted_data"
        }
        
        # Make POST request without Authorization header
        response = self.client.post(self.url, json=payload)
        
        # Assertions
        self.assertEqual(response.status_code, 401)
        self.assertIn("msg", response.json)
        self.assertEqual(response.json["msg"], "Missing Authorization Header")

if __name__ == "__main__":
    unittest.main()