from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ✅ ضَعْهما صراحةً هنا:
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# تطوير فقط
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# لا حاجة لــ SECURE_PROXY_SSL_HEADER محليًا؛ احذفها أو علّقها
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
