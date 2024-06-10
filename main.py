import timer, storage, ctypes
from actions import *
from art import tprint

TASKS = storage.load()

def start_menu() -> None:
    """
    Shows the user the start menu and processes their choice.
    """
    print_title()
    print("Overwhelmed with choices and don't know what to do first?\nLet me help you out :)\n")
    
    actions = [
        Action("Tell me what to do!", lambda: [pick_random_task(TASKS), start_menu()]), 
        Action("Edit tasks", task_menu),
        Action(f"Change timer length (currently {timer.format_seconds_duration(timer.get_length())})", lambda: [change_timer_length(), start_menu()])
    ]
    
    process_actions(actions, cancellable=False)

def task_menu(show_all: bool = False) -> None:
    """
    Shows the user the tasks they have and processes their choice.
    If show_all is True, all subtasks from the current task are shown recursively.
    """
    print_title()
    path = TASKS.path_str()
    if path: print(path)
    task_ids = TASKS.print_tasks(show_all)
    print()
    
    actions = [
        Action("Tell me what to do!", lambda: [pick_random_task(TASKS), task_menu(show_all)]),
        Action("Add task", lambda: [add_task(TASKS), task_menu(show_all)]),
        Action("Remove task", lambda: [remove_task(TASKS, task_ids), task_menu(show_all)]),
        Action("Rename task", lambda: [rename_task(TASKS, task_ids), task_menu(show_all)]),
        Action("Select task", lambda: [select_task(TASKS, task_ids), task_menu(show_all)]),
        Action("Collapse all tasks", task_menu) if show_all else Action("Expand all tasks", lambda: task_menu(show_all=True))
    ]
    if not TASKS.at_root(): actions += [
            Action("Back", lambda: [TASKS.back(), task_menu(show_all)]),
            Action("Back to top", lambda: [TASKS.back_to_root(), task_menu(show_all)])
        ]
    else: actions.append(Action("Back", start_menu))

    process_actions(actions, cancellable=False)

def print_title() -> None:
    clear_screen()
    tprint("Tell me what to do")


if __name__ == "__main__":
    # disable quick edit mode https://stackoverflow.com/questions/37500076/how-to-enable-windows-console-quickedit-mode-from-python
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
    
    start_menu()