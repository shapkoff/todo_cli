from datetime import datetime

import todo_cli.display as display
from todo_cli.database import DataBase
from todo_cli.status import Status
from todo_cli.task_model import TaskModel


def main() -> None:
    db: DataBase[str] = DataBase("tasks_db")

    display.greet_user()

    run = True
    while run:
        display.show_tasks(db.get_tasks())

        command: str = input("\nEnter a command (add, upd, del, exit): ")

        if command.lower() == "add":
            title: str = input("Enter task title: ")
            description: str = input("Enter task description: ")

            task = TaskModel(
                title=title,
                description=description,
                date=datetime.now(),
            )
            db.add_task(task)
            display.task_added()

        elif command.lower() == "upd":
            task_id = int(input("Enter task ID to update: "))
            task: TaskModel = db.get_task(task_id)

            title = input("Enter new task title (Enter to skip): ")
            description = input("Enter new task description (Enter to skip): ")
            status = int(
                input(
                    """Enter new task status: (Enter to skip)
                    (0: NONE, 1: IN_PROGRESS, 2: BLOCKED, 3: COMPLETED): """
                )
            )
            task.title = title if title else task.title
            task.description = description if description else task.description
            task.status = Status(status).value if status else task.status

            db.update_task(task)
            display.task_updated()

        elif command.lower() == "del":
            task_id = int(input("Enter task ID to delete: "))
            db.delete_task(task_id)
            display.task_deleted()

        elif command.lower() == "exit":
            run = False

        else:
            print("Invalid command. Please try again.")

    db.close_connection()


if __name__ == "__main__":
    main()
