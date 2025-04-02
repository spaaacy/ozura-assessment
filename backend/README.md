# Tokenization Service

This is a Flask-based tokenization service that uses MongoDB for storage and JWT for authentication.

## Prerequisites

1. **Python**: Ensure you have Python 3.8 or higher installed.
2. **MongoDB**: Install and run a MongoDB instance locally or provide a connection URI.
3. **Virtual Environment**: It's recommended to use a virtual environment to manage dependencies.

## Installation

Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:

   - **Windows**:
     ```bash
     py -3 -m venv .venv
     .venv\Scripts\activate
     ```

   - **macOS/Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file at the root of the project:
   ```plaintext
   ENCRYPTION_KEY=jZngpJFG2dNMmqCJdXGPRU5QfGJadyA8NYybBM3GfNQ=
   MONGO_URI=mongodb://localhost:27017/tokenization
   JWT_SECRET_KEY=324bd8c227e8074689c2b8f224d7fb10c47aa4e77590274cad048fa01f908456
   ```

5. Run the server:
   ```bash
   python main.py
   ```

## API Endpoints

The following endpoints are available:

### 1. **POST /register**
   - **Description**: Register a new user.
   - **Request Body**:
     ```json
     {
       "email": "user@example.com",
       "password": "securepassword"
     }
     ```
   - **Response**:
     - `201 Created`: User registration successful.
     - `400 Bad Request`: Missing email or password.
     - `409 Conflict`: User already exists.

### 2. **POST /login**
   - **Description**: Log in and receive a JWT token.
   - **Request Body**:
     ```json
     {
       "email": "user@example.com",
       "password": "securepassword"
     }
     ```
   - **Response**:
     - `200 OK`: Returns a JWT access token.
     - `400 Bad Request`: Missing email or password.
     - `401 Unauthorized`: Incorrect user credentials.

### 3. **POST /tokenize**
   - **Description**: Tokenize card details (requires JWT).
   - **Headers**:
     ```plaintext
     Authorization: Bearer <JWT_TOKEN>
     ```
   - **Request Body**:
     ```json
     {
       "card_number": "4111111111111111",
       "expiry": "12/25",
       "cvv": "123"
     }
     ```
   - **Response**:
     - `201 Created`: Returns a token for the card details.
     - `400 Bad Request`: Missing card details.

### 4. **POST /detokenize**
   - **Description**: Detokenize card details (requires JWT).
   - **Headers**:
     ```plaintext
     Authorization: Bearer <JWT_TOKEN>
     ```
   - **Request Body**:
     ```json
     {
       "token": "generated-token-id"
     }
     ```
   - **Response**:
     - `200 OK`: Returns the original card details.
     - `400 Bad Request`: Missing token.
     - `403 Forbidden`: User does not have access to the token.
     - `404 Not Found`: Token does not exist.
     - `500 Internal Server Error`: Decryption failed.

## Environment Variables

The application requires the following environment variables to be set in the `.env` file:

- `ENCRYPTION_KEY`: A 32-byte base64-encoded key for encrypting card details.
- `MONGO_URI`: MongoDB connection URI.
- `JWT_SECRET_KEY`: Secret key for signing JWT tokens.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.