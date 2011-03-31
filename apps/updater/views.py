from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from . import tasks


@never_cache
def update_preview(request, app_name):
    tasks.update_app.delay(app_name)
    return HttpResponse('success')
