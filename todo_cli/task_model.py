from dataclasses import dataclass
from datetime import datetime

from todo_cli.status import Status


@dataclass
class TaskModel:
    title: str
    date: datetime
    id: int | None = None
    description: str | None = None
    status: Status = Status.NONE
    edited: datetime | None = None

    def __post_init__(self) -> None:
        self.status = Status(self.status)

        if isinstance(self.date, str):
            self.date = datetime.fromisoformat(self.date).strftime(
                "%Y-%m-%d %H:%M"
            )

        if isinstance(self.edited, str) and self.edited != "None":
            self.edited = datetime.fromisoformat(self.edited).strftime(
                "%Y-%m-%d %H:%M"
            )
