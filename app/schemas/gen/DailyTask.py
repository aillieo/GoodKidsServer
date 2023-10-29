# generated by datamodel-codegen:
#   filename:  DailyTask.json

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class CompletionRecord(BaseModel):
    time: int
    note: Optional[str]


class DailyTask(BaseModel):
    id: int
    taskName: str
    taskDes: str
    lastRecord: Optional[CompletionRecord]
    reward: List[List[int]]
