import logging
from functools import partial

from celery import shared_task
from django.db import transaction

from apps.notifications.tasks import send_email

from .models import Dataset, DatasetRow
from .services import get_parsed_file

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True, bind=True, max_retries=3)
def process_dataset(self, dataset_id: int) -> None:
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
    except Dataset.DoesNotExist:
        logger.error("Dataset %s does not exist", dataset_id)
        return
    try:
        with transaction.atomic():
            dataset.status = dataset.Status.STARTED
            dataset.save(update_fields=["status"])
            df = get_parsed_file(dataset.file)
            rows = [
                DatasetRow(dataset=dataset, data=row.to_dict(), row_index=index)
                for (index, row) in df.iterrows()
            ]
            DatasetRow.objects.bulk_create(rows, batch_size=1000)
            dataset.status = dataset.Status.SUCCESS
            dataset.columns = list(df.columns)
            dataset.save(update_fields=["status", "columns"])
        # on commit ensures email is sent only after the transaction
        # is committed, preventing notification on rollback.
        transaction.on_commit(
            partial(
                send_email.delay,
                dataset.user.id,
                "Ваш датасет был обработан!",
                "Датасет был обработан!\n Скорее заходите проверить!",
            )
        )
    except Exception as exc:
        logger.error("process_dataset %s failed: %s", dataset_id, exc)
        if self.request.retries == self.max_retries:
            dataset.status = dataset.Status.FAILURE
            dataset.save(update_fields=["status"])
            send_email.delay(
                dataset.user.id,
                "Ваш датасет не был обработан:(",
                "Произошла ошибка при обработке датасета. Попробуйте загрузить файл снова.",
            )
            return
        raise self.retry(exc=exc)
