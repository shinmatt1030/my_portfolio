from .settings_common import *


# デバッグモードを有効にするかどうか(本番運用では必ずFalseにする)
DEBUG = False

# 許可するホスト名のリスト
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

# 静的ファイルを配置する場所
STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'

# Amazon SES関連設定
AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_REGION_NAME = 'ap-northeast-1'
AWS_SES_REGION_ENDPOINT = 'email-smtp.ap-northeast-1.amazonaws.com'

# sendgrid使用設定
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'

# ロギング
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        # diaryアプリケーションが利用するロガー
        'diary': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },

    # ハンドラの設定
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D',  # ログローテーション(新しいファイルへの切り替え)間隔の単位(D=日)
            'interval': 1,  # ログローテーション間隔(1日単位)
            'backupCount': 7,  # 保存しておくログファイル数
        },
    },

    # フォーマッタの設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

# セキュリティ関連設定
# security.W004
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# security.W006
SECURE_CONTENT_TYPE_NOSNIFF = True
# security.W007
SECURE_BROWSER_XSS_FILTER = True
# security.W008
# SECURE_SSL_REDIRECT = True
# security.W012
SESSION_COOKIE_SECURE = True
# security.W016
CSRF_COOKIE_SECURE = True
# security.W019
X_FRAME_OPTIONS = 'DENY'
# security.W021
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')