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


def paginated_response(message: str, data: Any, page: int, page_size: int, total: int) -> dict:
    return success_response(
        message=message,
        data=data,
        pagination={
            "page": page,
            "page_size": page_size,
            "total": total,
        },
    )


def error_response(message: str, code: str, details: str) -> dict:
    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details,
        },
    }
