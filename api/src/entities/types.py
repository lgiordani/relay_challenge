from typing import TypedDict

LineItemType = TypedDict(
    "LineItemType", {"name": str, "quantity": int, "rate": float, "total": float}
)

ActivityLogType = TypedDict(
    "ActivityLogType", {"route_id": str, "attempt_date_time": str, "success": bool}
)
