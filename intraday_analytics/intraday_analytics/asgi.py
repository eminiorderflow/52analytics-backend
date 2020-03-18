import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intraday_analytics.settings")
django.setup()
application = get_default_application()
