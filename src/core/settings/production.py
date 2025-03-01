from .base import *  # noqa

# SECURITY
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")  # noqa

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")  # noqa
EMAIL_PORT = env("EMAIL_PORT")  # noqa
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # noqa
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # noqa
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")  # noqa
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")  # noqa
