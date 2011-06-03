import json
from subprocess import Popen, PIPE, STDOUT

from celery.task import task
from django.conf import settings
import redisutils


def run(script):
    p = Popen(script, stdout=PIPE, stderr=STDOUT, shell=True)
    out, err = p.communicate()
    return p.returncode, out, err


@task(ignore_result=True)
def update_app(name, payload):
    redis = redisutils.connections['master']
    lock = redis.lock('updater.%s' % name, timeout=300)

    try:
        app_config = settings.APP_UPDATERS[name]
    except KeyError:
        return

    if 'ref' in app_config and payload['ref'] != app_config['ref']:
        return

    if not lock.acquire(False):
        redis.publish('update.%s.locked' % name, json.dumps(payload))
        update_app.retry()

    script = app_config['script']
    outfile = app_config.get('outfile')

    l = update_app.get_logger()
    l.info("Running: %s" % script)
    redis.publish('update.%s' % name, json.dumps(payload))

    rv = run(script)

    if outfile:
        with open(outfile, 'w') as f:
            f.write(rv[1])

    redis.publish('update.%s' % name, json.dumps(rv + (payload,)))
    l.info("Finished updating.")
    lock.release()
