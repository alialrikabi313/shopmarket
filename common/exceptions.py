from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
resp = exception_handler(exc, context)
if resp is not None:
detail = resp.data.get("detail", "Request failed") if isinstance(resp.data, dict) else str(resp.data)
resp.data = {"error": {"code": resp.status_code, "message": detail, "details": resp.data}}
return resp