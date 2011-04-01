import json
from subprocess import Popen, PIPE

from celery.task import task
from django.conf import settings
import redisutils


def run(script):
    p = Popen(script, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    return p.returncode, out, err


@task(ignore_result=True)
def update_app(name, payload):
    redis = redisutils.connections['master']

    try:
        script = settings.APP_UPDATERS[name]
    except KeyError:
        return

    l = update_app.get_logger()
    l.info("Running: %s" % script)
    redis.publish('update.%s' % name, payload)
    rv = run(script)
    redis.publish('update.%s' % name, json.dumps(rv + (payload,)))
    l.info("Finished updating.")
