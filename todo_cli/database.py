import os
import sqlite3
from datetime import datetime
from sqlite3 import Connection, Cursor

from todo_cli.status import Status
from todo_cli.task_model import TaskModel


class DataBase:
    def __init__(self, db_name) -> None:
        self.database_path: str = f"{os.getcwd()}\\{db_name}.db"
        self.connection: Connection = sqlite3.connect(self.database_path)
        self.cursor: Cursor = self.connection.cursor()

    def create_table(self) -> None:
        self.cursor.execute("""CREATE TABLE "Task" (
                "id"	INTEGER NOT NULL UNIQUE,
                "title"	TEXT NOT NULL,
                "description"	TEXT,
                "status"	INTEGER NOT NULL,
                "date"	TEXT NOT NULL,
                "edited"	INTEGER DEFAULT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );""")
        self.connection.commit()

    def get_task(self, task_id) -> TaskModel:
        query: Cursor = self.cursor.execute(
            f"""SELECT * FROM Task
                WHERE id = {task_id};"""
        )
        respons: tuple = query.fetchone()

        task_model = TaskModel(
            id=respons[0],
            title=respons[1],
            description=respons[2],
            status=respons[3],
            date=respons[4],
            edited=respons[5],
        )

        return task_model

    def get_tasks(self) -> list[TaskModel]:
        query: Cursor = self.cursor.execute("""SELECT * FROM Task;""")
        respons: list[tuple] = query.fetchall()

        task_list: list[TaskModel] = []
        for task in respons:
            task_model = TaskModel(
                id=task[0],
                title=task[1],
                description=task[2],
                status=task[3],
                date=task[4],
                edited=task[5],
            )
            task_list.append(task_model)

        return task_list

    def add_task(self, task) -> None:
        query: Cursor = self.cursor.execute(
            f"""INSERT INTO Task (title, description, status, date, edited)
                VALUES
                ('{task.title}', '{task.description}', {task.status.value},
                '{str(task.date)}', '{str(task.edited)}');"""
        )
        query.fetchone()

        self.connection.commit()

    def update_task(self, task) -> None:
        query: Cursor = self.cursor.execute(
            f"""UPDATE Task
                SET status = {Status(task.status).value},
                title = '{task.title}',
                description = '{task.description}',
                edited = '{str(datetime.now())}'
                WHERE id = {task.id};"""
        )
        query.fetchone()

        self.connection.commit()

    def delete_task(self, task_id):
        query: Cursor = self.cursor.execute(
            f"""DELETE FROM Task
                WHERE id = {task_id};"""
        )
        query.fetchone()

        self.connection.commit()

    def close_connection(self):
        self.connection.close()
