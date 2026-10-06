"""Password hashing with bcrypt (used directly; passlib is unmaintained).

Hashes created earlier through passlib use the same "$2b$" bcrypt format,
so existing users can still log in.
"""
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        # Malformed or non-bcrypt hash stored in the database.
        return False


# Used to keep login timing similar when the email does not exist.
DUMMY_PASSWORD_HASH = hash_password("timing-equalizer-not-a-real-password")
