from typing import Callable
from os import system, name
from collections import namedtuple
from data_structures.task_tree import TaskTree
import sys, string, random, storage, settings, timer

Action = namedtuple("Action", ["description", "function"])
ALPHABET = list(string.ascii_lowercase)

def clear_screen() -> None:
    """
    Clears the screen.
    """
    system('cls' if name == 'nt' else 'clear')

def process_actions(actions: list[Action], input_prompt: str = "", cancellable: bool = True) -> None:
    """
    Processes a list of actions, displaying them to the user and
    executing the chosen one.
    """
    action_map = dict()
    for i in range(len(actions)):
        key, action = ALPHABET[i], actions[i]
        action_map[key] = action
        print(f"{key}. {action.description}")
    print()

    action_map["q"] = Action("", sys.exit) # hidden quit action
    choice = get_valid_input(lambda x: x in action_map, input_prompt, cancellable)
    action_map[choice].function()

def pick_random_task(tasks: TaskTree) -> None:
    clear_screen()
    if len(tasks) == 0:
        print("No tasks to choose from.")
        system("pause")
        return

    chosen_task = random.choice(tasks)
    print("Chosen task:")
    path = tasks.path_str(chosen_task)
    if path: print(path)
    print(chosen_task.name + "\n\n")
    timer.start()

def add_task(tasks: TaskTree) -> None:
    task_name = get_valid_input(prompt="Enter task name: ")
    if task_name:
        tasks.add_task(task_name)
        storage.save(tasks)

def remove_task(tasks: TaskTree, task_ids: set[str]) -> None:
    task_id = get_valid_input(lambda x: x in task_ids, "Enter task number to remove: ")
    if task_id:
        tasks.remove(task_id)
        storage.save(tasks)

def rename_task(tasks: TaskTree, task_ids: set[str]) -> None:
    task_id = get_valid_input(lambda x: x in task_ids, "Select task number to rename: ")
    if task_id:
        new_name = get_valid_input(prompt="Enter new task name: ")
        if new_name:
            tasks.rename(task_id, new_name)
            storage.save(tasks)

def select_task(tasks: TaskTree, task_ids: set[str]) -> None:
    task_id = get_valid_input(lambda x: x in task_ids, "Enter task number to select: ")
    if task_id:
        tasks.into(task_id)

def change_timer_length() -> None:
    new_length = get_valid_input(lambda x: x.isdecimal(), "Enter new timer length in minutes: ")
    if new_length:
        settings.set("timer_length", int(new_length) * 60)

def get_valid_input(condition: Callable[[str], bool] = None, prompt: str = "", cancellable: bool = True) -> str:
    """
    Given a condition to check whether the user's input is valid, keep
    asking for input until a valid one is provided or the user cancels.
    """
    try:
        if cancellable: print("Ctrl+C to cancel")
        if not condition:
            choice = input(prompt if prompt else "> ")
            print() # newline after input
            return choice
        
        while True:
            choice = input(prompt if prompt else "> ").strip(" .").lower()
            if condition(choice):
                print() # newline after valid input
                return choice
            
            print("\033[F\033[K", end="") # clear input line

    except KeyboardInterrupt:
        if not cancellable:
            sys.exit()


if __name__ == "__main__":
    pass