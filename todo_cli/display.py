from prettytable import PrettyTable, TableStyle


class Display:
    table = PrettyTable()
    table.field_names = [
        "ID",
        "Title",
        "Description",
        "Status",
        "Date",
        "Edited",
    ]
    table.set_style(TableStyle.SINGLE_BORDER)

    _greeted = False

    @classmethod
    def show_tasks(cls, tasks: list) -> None:
        if not cls._greeted:
            cls.greet_user()
            cls._greeted = True

        for task in tasks:
            cls.table.add_row(
                [
                    task.id,
                    task.title,
                    task.description,
                    task.status.name,
                    task.date,
                    task.edited if task.edited else "No",
                ]
            )
        print(cls.table)
        cls.table.clear_rows()

    @staticmethod
    def greet_user() -> None:
        print("\nWelcome to the To-Do CLI Application!")
        print("Here are your current tasks:\n")

    @staticmethod
    def task_added() -> None:
        print("\nTask added successfully\n")

    @staticmethod
    def task_updated() -> None:
        print("\nTask updated successfully\n")

    @staticmethod
    def task_deleted() -> None:
        print("\nTask deleted successfully\n")
