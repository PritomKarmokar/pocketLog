def format_success_response(response: dict, data: dict) -> dict:
    if data:
        response['data'] = data
    return response