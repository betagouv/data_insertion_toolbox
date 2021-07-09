from cryptography.fernet import Fernet
import os


def get_encryption_tool():
  return Fernet(os.getenv('HUBEE_SHARED_SECRET'))
