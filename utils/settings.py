from passlib.context import CryptContext

password_manager = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")