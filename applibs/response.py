def format_output_success(response: dict, data: dict) -> dict:
    if data:
        response['data'] = data
    return response

def format_output_error(response: dict, error: str) -> dict:
    if error:
        response['error'] = error
    return response