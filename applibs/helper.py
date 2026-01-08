from typing import Optional

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