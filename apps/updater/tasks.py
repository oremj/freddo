from subprocess import Popen, PIPE


from celery.task import task
from django.conf import settings


def run(script):
    return Popen(script, stdout=PIPE, stderr=PIPE, shell=True).communicate()

@task
def update_app(name):
    try:
        script = settings.APP_UPDATERS[name]
    except KeyError:
        return
    l = update_app.get_logger()
    l.info("Running: %s" % script)
    run(script)
    l.info("Finished updating.")
    return True
