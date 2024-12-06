import os
from cryptography.fernet import Fernet



class Authentication: 
    def generate_key(self):
        """Generate and return a new key for encryption."""
        return Fernet.generate_key()

    def save_key(self, key):
        """Save the encryption key to a file."""
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        """Load the encryption key from a file."""
        return open("secret.key", "rb").read()

    def encrypt_credentials(self, username, password):
        """Encrypt the username and password."""
        key = self.generate_key()
        self.save_key(key)
        fernet = Fernet(key)
        encrypted_username = fernet.encrypt(username.encode())
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_username, encrypted_password

    def decrypt_credentials(self, encrypted_username, encrypted_password):
        """Decrypt the username and password."""
        key = self.load_key()
        fernet = Fernet(key)
        username = fernet.decrypt(encrypted_username).decode()
        password = fernet.decrypt(encrypted_password).decode()
        return username, password

    def load_credentials(self):
        """Load credentials from a file or request input from the user."""
        if os.path.exists("credentials.txt"):
            with open("credentials.txt", "rb") as f:
                encrypted_username, encrypted_password = f.read().split(b"\n")
                return self.decrypt_credentials(encrypted_username, encrypted_password)
        else:
            username = input("Enter your roller's email: ")
            password = input("Enter your password: ")
            encrypted_username, encrypted_password = self.encrypt_credentials(
                username, password
            )
            with open("credentials.txt", "wb") as f:
                f.write(encrypted_username + b"\n")
                f.write(encrypted_password)
            return username, password
