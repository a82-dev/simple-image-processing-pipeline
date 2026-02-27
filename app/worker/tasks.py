import time

from app.worker.celery_app import celery_app
from app.worker.image_utils import apply_heavy_filter


@celery_app.task(bind=True, max_retries=3)
def filter_image_task(self, filename: str):
    try:
        # fake sleep just to see the flow
        time.sleep(10)

        output_file = apply_heavy_filter(filename)

        return {"status": "success", "file": output_file}

    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
