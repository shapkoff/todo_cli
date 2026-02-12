from prettytable import PrettyTable, TableStyle

TABLE = PrettyTable()

TABLE.field_names = [
    "ID",
    "Title",
    "Description",
    "Status",
    "Date",
    "Edited",
]
TABLE.set_style(TableStyle.SINGLE_BORDER)


def show_tasks(tasks: list) -> None:
    for task in tasks:
        TABLE.add_row(
            [
                task.id,
                task.title,
                task.description,
                task.status.name,
                task.date.strftime("%Y-%m-%d %H:%M"),
                task.edited.strftime("%Y-%m-%d %H:%M")
                if task.edited
                else "No",
            ]
        )
    print(TABLE)
    TABLE.clear_rows()


def greet_user() -> None:
    print("\nWelcome to the To-Do CLI Application!")
    print("Here are your current tasks:\n")


def task_added() -> None:
    print("\nTask added successfully\n")


def task_updated() -> None:
    print("\nTask updated successfully\n")


def task_deleted() -> None:
    print("\nTask deleted successfully\n")
