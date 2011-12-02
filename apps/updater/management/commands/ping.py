from django.core.management.base import BaseCommand

import celery.task


class Command(BaseCommand):
    def handle(self, *a, **kw):
        celery.task.control.ping()
