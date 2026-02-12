from dataclasses import dataclass, field
from datetime import datetime

from todo_cli.status import Status


@dataclass
class TaskModel:
    title: str
    date: datetime = field(default_factory=datetime.now)
    id: int | None = None
    description: str | None = None
    status: Status = Status(0)
    edited: datetime | None = None

    def __post_init__(self) -> None:
        if isinstance(self.date, str):
            self.date = datetime.fromisoformat(self.date)

        if self.edited == "None":
            self.edited = None
        elif isinstance(self.edited, str):
            self.edited = datetime.fromisoformat(self.edited)
