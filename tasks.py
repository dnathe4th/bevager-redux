from celery import Celery

from bevager_cli import BevagerClient
from datastore import persist_rum_for_user

app = Celery('bevager', broker='redis://')
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_ENABLE_UTC=True,
)


@app.task
def test():
    return 'OK'


@app.task
def load_rums(user=None):
    client = BevagerClient(user=user)
    client.login()

    resp = client.load_rum_list_html()
    rums = client.extract_rum_list_data(resp.text)

    for rum in rums:
        save_rum.delay(rum, user)


@app.task
def save_rum(rum, user):
    return persist_rum_for_user(rum, user)
