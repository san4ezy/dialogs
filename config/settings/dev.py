from .base import *


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=100),
    'REFRESH_TOKEN_TIMELINE': timedelta(hours=1000),
}
