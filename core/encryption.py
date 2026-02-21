# core/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings

cipher = Fernet(settings.ENCRYPTION_KEY)

def encrypt(value):
    return cipher.encrypt(value.encode()).decode()

def decrypt(value):
    return cipher.decrypt(value.encode()).decode()
 