from celery import shared_task
import logging
logger = logging.getLogger(__name__)


@shared_task
def analyze_data():
    logger.info("task started")

    try:
        result = {
            'status': 'success',
            'analyzed_count': 100,
            'message': 'data analyzed',
        }
        logger.info(result)
        return result

    except Exception as e:
        logger.error(str(e))
        raise
