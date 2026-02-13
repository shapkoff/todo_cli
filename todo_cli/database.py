import sqlite3
from datetime import datetime
from pathlib import Path
from sqlite3 import Connection, Cursor

from todo_cli.status import Status
from todo_cli.task_model import TaskModel


class DataBase:
    def __init__(self, db_name) -> None:
        self.database_path: Path = Path.cwd() / f"{db_name}.db"

    def __enter__(self):
        self.connection: Connection = sqlite3.connect(self.database_path)
        self.cursor: Cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def create_table(self) -> None:
        query = """CREATE TABLE "Task" (
                "id"	INTEGER NOT NULL UNIQUE,
                "title"	TEXT NOT NULL,
                "description"	TEXT,
                "status"	INTEGER NOT NULL,
                "date"	TEXT NOT NULL,
                "edited"	INTEGER DEFAULT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );"""
        self.cursor.execute(query)
        self.connection.commit()

    def get_task(self, task_id) -> TaskModel:
        query: str = """SELECT * FROM Task WHERE id = ?;"""
        data = [task_id]
        response: tuple = self.cursor.execute(query, data).fetchone()

        task_model = TaskModel(
            id=response[0],
            title=response[1],
            description=response[2],
            status=Status(response[3]),
            date=response[4],
            edited=response[5],
        )

        return task_model

    def get_tasks(self) -> list[TaskModel]:
        query: str = """SELECT * FROM Task;"""
        response: list[tuple] = self.cursor.execute(query).fetchall()

        task_list: list[TaskModel] = []
        for task in response:
            task_model = TaskModel(
                id=task[0],
                title=task[1],
                description=task[2],
                status=Status(task[3]),
                date=task[4],
                edited=task[5],
            )
            task_list.append(task_model)

        return task_list

    def add_task(self, task) -> None:
        query: str = """INSERT INTO Task (title, description,
                        status, date, edited)
                        VALUES (?, ?, ?, ?, ?);"""
        data = [
            task.title,
            task.description,
            task.status.value,
            task.date,
            task.edited,
        ]
        self.cursor.execute(query, data)
        self.connection.commit()

    def update_task(self, task) -> None:
        query: str = """UPDATE Task SET status = ?, title = ?,
                        description = ?, edited = ? WHERE id = ?;"""

        data = [
            task.status.value,
            task.title,
            task.description,
            datetime.now(),
            task.id,
        ]
        self.cursor.execute(query, data)
        self.connection.commit()

    def delete_task(self, task_id):
        query: str = """DELETE FROM Task WHERE id = ?;"""
        data = [task_id]
        self.cursor.execute(query, data)

        self.connection.commit()
