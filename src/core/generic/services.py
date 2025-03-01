import base64
import hashlib
import time

from cryptography.fernet import Fernet
from django.conf import settings
from django.core.cache import cache
from django.core.signing import BadSignature, TimestampSigner


class TokenService:
    def __init__(self, secret_key=None, salt="secure-token"):
        self.secret_key = secret_key or settings.SECRET_KEY
        self.salt = salt
        self.signer = TimestampSigner(salt=self.salt)
        self.fernet = self._get_fernet_cipher()

    def _get_fernet_cipher(self):
        """Genera una clave de encriptación segura basada en SECRET_KEY y la salt"""
        key_material = hashlib.sha256(f"{self.secret_key}{self.salt}".encode()).digest()
        fernet_key = base64.urlsafe_b64encode(key_material[:32])
        return Fernet(fernet_key)

    def generate_token(self, user_id, action, expires_in=3600):
        """
        Genera un token seguro encriptado y firmado.
        """
        expiration_timestamp = int(time.time()) + expires_in
        raw_data = f"{user_id}:{action}:{expiration_timestamp}".encode()
        encrypted_data = self.fernet.encrypt(raw_data)
        return self.signer.sign(encrypted_data.decode())

    def validate_token(self, token, expected_action):
        """
        Valida un token encriptado y firmado, verificando si ya ha sido usado.
        """
        try:
            signed_data = self.signer.unsign(token)
            decrypted_data = self.fernet.decrypt(signed_data.encode()).decode()
            user_id, action, expiration_timestamp = decrypted_data.split(":")
            expiration_timestamp = int(expiration_timestamp)

            # Verificar si el token ha expirado
            if time.time() > expiration_timestamp:
                return None

            # Verificar si la acción es la esperada
            if action != expected_action:
                return None

            # Verificar si el token ya fue usado (está en caché)
            if cache.get(f"invalidated_token:{token}"):
                return None

            return int(user_id)

        except (BadSignature, ValueError, Exception):
            return None

    def invalidate_token(self, token):
        """
        Invalida un token después de su uso.
        """
        cache.set(f"invalidated_token:{token}", True, timeout=3600)
