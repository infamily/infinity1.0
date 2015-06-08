LOCAL_APPS = (
    'core',
)

CONSTANCE_CONFIG = {
}

AUTH_USER_MODELS = [
    "core.User",
]

"""
    Set default auth user model from models list
    if AUTH_USER_MODELS is empty, set django user model by default
"""

AUTH_USER_MODEL = AUTH_USER_MODELS[0] if AUTH_USER_MODELS else 'auth.User'

LOGIN_URL = '/login/'

STRIPE_PUBLIC_KEY = 'pk_test_4RWCT2Iq1FcyU7kZCqGPaZds'
STRIPE_SECRET_KEY = 'sk_test_4RWC8fp7U55VayXPT5D6lzJt'

DJSTRIPE_PLANS = {
    "monthly": {
        "stripe_plan_id": "pro-monthly",
        "name": "Web App Pro ($25/month)",
        "description": "The monthly subscription plan to WebApp",
        "price": 2500,  # $25.00
        "currency": "usd",
        "interval": "month"
    },
    "yearly": {
        "stripe_plan_id": "pro-yearly",
        "name": "Web App Pro ($199/year)",
        "description": "The annual subscription plan to WebApp",
        "price": 19900,  # $19900
        "currency": "usd",
        "interval": "year"
    },
    "day": {
        "stripe_plan_id": "one-day",
        "name": "Web App Pro ($100000/year)",
        "description": "One day",
        "price": 800000,  # $19900
        "currency": "usd",
        "interval": "day",
    },
    "gold": {
        "stripe_plan_id": "gold",
        "name": "Gold ($199/year)",
        "description": "The annual subscription plan to Gold",
        "price": 20000,  # $19900
        "currency": "usd",
        "interval": "year",
        "trial_period_days": 30
    }
}

# Some autoslag handler that we need to create for make tests runnable


def auto_slag_handler():
    return 'auto_slug'

MOMMY_CUSTOM_FIELDS_GEN = {
    'django_extensions.db.fields.AutoSlugField': auto_slag_handler,
}
