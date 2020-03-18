from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import django
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intraday_analytics.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
django.setup()

app = Celery('intraday_analytics')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
