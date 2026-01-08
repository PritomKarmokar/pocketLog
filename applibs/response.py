def format_output_success(response: dict, data: dict) -> dict:
    if data:
        response['data'] = data
    return response