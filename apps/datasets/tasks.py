import logging

from celery import shared_task

from .models import Dataset, DatasetRow
from .services import get_parsed_file

logger = logging.getLogger(__name__)


@shared_task
def process_dataset(dataset_id: int) -> None:
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
    except Dataset.DoesNotExist:
        logger.error(f"Dataset {dataset_id} does not exist")
        return
    try:
        dataset.status = dataset.Status.STARTED
        dataset.save(update_fields=["status"])
        df = get_parsed_file(dataset.file)
        rows = [
            DatasetRow(dataset=dataset, data=row.to_dict(), row_index=index)
            for (index, row) in df.iterrows()
        ]
        DatasetRow.objects.bulk_create(rows, batch_size=1000)
        dataset.status = dataset.Status.SUCCESS
        dataset.save(update_fields=["status"])
    except Exception as e:
        logger.error(f"process_dataset {dataset_id} failed: {e}")
        dataset.status = dataset.Status.FAILURE
        dataset.save(update_fields=["status"])
