from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

import models
import schemas
import utils


class SchemaUtils():

    @staticmethod
    def convert_daily_task(daily_task_db: models.DailyTask) -> schemas.DailyTask:
        dict: Dict[str, Any] = vars(daily_task_db)
        completion_record: Optional[models.CompletionRecord] = daily_task_db.completion_records[-1] if daily_task_db.completion_records else None
        dict["lastRecord"] = SchemaUtils.convert_completion_record(
            completion_record) if completion_record else None
        daily_task: schemas.DailyTask = schemas.DailyTask(**dict)
        return daily_task

    @staticmethod
    def convert_completion_record(completion_record_db: models.CompletionRecord) -> schemas.CompletionRecord:
        dict: Dict[str, Any] = vars(completion_record_db)
        dict["time"] = utils.get_timestamp(dict["time"])
        completion_record: schemas.CompletionRecord = schemas.CompletionRecord(
            **dict)
        return completion_record
