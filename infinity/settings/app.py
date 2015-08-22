LOCAL_APPS = (
    'users',
    'core',
    'payments',
)

CONSTANCE_CONFIG = {
    'PAYPAL_MODE': ('sandbox', 'sandbox or live'),
    'PAYPAL_APPLICATION_ID': ('APP-80W284485P519543T', 'PayPal application ID'),
    'PAYPAL_SECURITY_USERID': ('shamkir-facilitator_api1.gmail.com', 'PayPal security user id'),
    'PAYPAL_SECURITY_PASSWORD': ('HATJ3CEGRHZVQTZV', 'PayPal security password'),
    'PAYPAL_SECURITY_SIGNATURE': ('AFcWxV21C7fd0v3bYYYRCpSSRl31AU7eDuvOQwePEQhUEjtkBesDYrC.', 'PayPal security signature'),
    'PAYPAL_CANCEL_URL': ('http://localhost:3000/', 'PayPal cancel URL'),
    'MAX_MENTIONS_PER_COMMENT': (10, '_comment_post_save email notifications per comment')
}

AUTH_USER_MODELS = [
    "users.User",
]

"""
    Set default auth user model from models list
    if AUTH_USER_MODELS is empty, set django user model by default
"""

AUTH_USER_MODEL = "users.User"

LOGIN_URL = '/user/login/'

# Some autoslag handler that we need to create for make tests runnable


def auto_slag_handler():
    return 'auto_slug'


def auto_markdown_field_gen():
    return 'auto_markdown'

MOMMY_CUSTOM_FIELDS_GEN = {
    'django_extensions.db.fields.AutoSlugField': auto_slag_handler,
    'django_markdown.models.MarkdownField': auto_markdown_field_gen
}
