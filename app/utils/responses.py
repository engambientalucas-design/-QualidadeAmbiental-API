from typing import Any, Optional


def success_response(
    message: str,
    data: Any = None,
    pagination: Optional[dict] = None,
) -> dict:
    response = {
        "success": True,
        "message": message,
        "data": data,
    }

    if pagination is not None:
        response["pagination"] = pagination

    return response


def error_response(message: str, code: str, details: str) -> dict:
    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details,
        },
    }
