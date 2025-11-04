from passlib.hash import argon2
import hashlib
import hmac

def hash_password(password: str) -> str:
    # fallback to regular argon2 if argon2id not available
    try:
        return argon2.using(type="argon2id").hash(password)
    except ValueError:
        return argon2.hash(password)

def verify_password(password: str, hash_: str) -> bool:
    try:
        return argon2.verify(password, hash_)
    except Exception:
        return False

def hash_token(token: str) -> str:
    # simple SHA256 hex digest for storing refresh token hashes
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def secure_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)
