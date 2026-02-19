from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME', default='/touragency_proj')