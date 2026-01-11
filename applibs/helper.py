import hmac
import hashlib
from typing import Optional
from django.conf import settings

from applibs.status import (
    VALID_DATA_NOT_FOUND,
    VALIDATION_ERROR_DICT
)

def handle_validation_error(errors: dict) -> Optional[str]:
    for error in errors.items():
        print(error)
        return error[1][0].code
    return None

def render_serializer_errors(errors: dict) -> dict:
    error_code = handle_validation_error(errors)
    return VALIDATION_ERROR_DICT.get(error_code, VALID_DATA_NOT_FOUND)

def generate_hashed_token(token: str) -> str:
    hash_key = settings.PASSWORD_CHANGE_REQUEST_HASH_KEY
    encoded_data = token.encode('utf-8') # converting `token` to bytes
    encoded_hash_key = hash_key.encode('utf-8')
    return hmac.new(encoded_hash_key, encoded_data, hashlib.sha256).hexdigest()

def verify_token(raw_code: str, stored_hash: str) -> bool:
    return hmac.compare_digest(
        generate_hashed_token(raw_code),
        stored_hash
    )