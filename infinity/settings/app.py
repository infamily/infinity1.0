LOCAL_APPS = (
    'core',
    'payments'
)

CONSTANCE_CONFIG = {
    'PAYPAL_MODE': ('sandbox', 'sandbox or live'),
    'PAYPAL_SECURITY_USERID': ('shamkir-facilitator_api1.gmail.com', 'PayPal security user id'),
    'PAYPAL_SECURITY_PASSWORD': ('HATJ3CEGRHZVQTZV', 'PayPal security password'),
    'PAYPAL_SECURITY_SIGNATURE': ('AFcWxV21C7fd0v3bYYYRCpSSRl31AU7eDuvOQwePEQhUEjtkBesDYrC.', 'PayPal security signature'),
    'PAYPAL_CANCEL_URL': ('http://localhost:3000/', 'PayPal cancel URL')

}

AUTH_USER_MODELS = [
    "core.User",
]

"""
    Set default auth user model from models list
    if AUTH_USER_MODELS is empty, set django user model by default
"""

AUTH_USER_MODEL = "core.User"

LOGIN_URL = '/login/'

# Some autoslag handler that we need to create for make tests runnable


def auto_slag_handler():
    return 'auto_slug'

MOMMY_CUSTOM_FIELDS_GEN = {
    'django_extensions.db.fields.AutoSlugField': auto_slag_handler,
}
