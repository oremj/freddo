from django.http import HttpResponse

from . import tasks

def update_preview(request, app_name):
    tasks.update_app.delay(app_name)
    return HttpResponse('success')
