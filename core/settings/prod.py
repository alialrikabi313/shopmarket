# core/settings/prod.py
from .base import *  # noqa
import os
from datetime import timedelta
import dj_database_url

# تشغيل الإنتاج
DEBUG = False

# السماح بالمضيف (Render يوفّر متغير RENDER_EXTERNAL_HOSTNAME تلقائيًا)
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
ALLOWED_HOSTS = [h for h in [_render_host, "localhost", "127.0.0.1"] if h]

# مهم جدًا في Django 4/5: يجب تضمين البروتوكول
CSRF_TRUSTED_ORIGINS = [f"https://{_render_host}"] if _render_host else []

# أمان خلف البروكسي (Render يعمل خلف HTTPS)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# السر من البيئة (لا تضع مفتاحًا صريحًا هنا)
SECRET_KEY = "_[1uSKG;]q0z*?6=E:2lu/.mNZv|,u97r-Ady3vb?PdOS'9ZgyaO_wV\\@wa`AQ86"

# ترتيب الميدلوير في الإنتاج + WhiteNoise للستايتك
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # لازم يجي بعد Security
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ملفات الستاتيك عبر WhiteNoise
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# الميديا (محلية = غير دائمة على Render). لاحقًا نقدر ننقل Cloudinary/S3
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# قاعدة البيانات من DATABASE_URL (PostgreSQL على Render). إن ماكو، يسقط إلى SQLite
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR/'db.sqlite3'}"),
        conn_max_age=600,
    )
}

# السماح CORS مؤقتًا (اختياري: ضيّقها لاحقًا لدومين تطبيق Flutter فقط)
CORS_ALLOW_ALL_ORIGINS = True

# إعدادات JWT (نفس التطوير)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
