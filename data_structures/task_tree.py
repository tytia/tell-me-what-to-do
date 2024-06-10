from typing import Iterator
from data_structures.task_node import TaskNode

class TaskTree:
    """
    Essentially a file system tree. Each task/node has a name and can have subtasks/children.
    Operations are performed based on the current task/node, not the whole tree.
    """

    def __init__(self, root: TaskNode = None) -> None:
        self.root = root if root else TaskNode("root", [])
        self.curr = self.root

    @classmethod
    def from_JSON_object(cls, data: dict) -> 'TaskTree':
        """
        Reconstructs a TaskTree from a JSON object.
        """
        return cls(TaskNode.from_JSON_object(data))

    def add_task(self, name: str) -> None:
        self.curr.add_child(TaskNode(name))

    def add_tasks(self, names: list[str]) -> None:
        for name in names:
            self.add_task(name)

    def remove(self, task_id: str) -> None:
        """
        Removes the task of the specified id.
        Assumes the task id is valid.
        """
        task_id = list(map(lambda x: int(x) - 1, task_id.split(".")))
        curr = self.curr
        for i in range(len(task_id) - 1):
            curr = curr.subtasks[task_id[i]]
        
        curr.remove_child(task_id[-1])
    
    def into(self, task_id: str) -> None:
        """
        Go into the task of the specified id.
        Assumes the task id is valid.
        """
        task_id = list(map(lambda x: int(x) - 1, task_id.split(".")))
        for i in task_id:
            self.curr = self.curr.subtasks[i]
    
    def rename(self, task_id: str, new_name: str) -> None:
        """
        Renames the task of the specified id.
        Assumes the task id is valid.
        """
        task_id = list(map(lambda x: int(x) - 1, task_id.split(".")))
        curr = self.curr
        for i in range(len(task_id) - 1):
            curr = curr.subtasks[task_id[i]]
        
        curr.subtasks[task_id[-1]].name = new_name

    def back(self) -> None:
        """
        Return to previous parent task (cd ..)
        """
        if self.at_root():
            print("Already at root, can't go back any further.")
            return

        self.curr = self.curr.parent

    def back_to_root(self) -> None:
        """
        Return to the root task.
        """
        self.curr = self.root

    def at_root(self) -> bool:
        return self.curr == self.root
    
    def print_tasks(self, recursive: bool = False) -> set[str]:
        """
        Prints the subtasks of the current task.
        If recursive is True, prints all subtasks recursively.

        Returns a set of the tasks' ids.
        """
        task_ids = set()
        if not self.curr.subtasks:
            print(f"There are currently no tasks under \"{self.curr.name}\".")
            return task_ids
        
        if recursive:
            return self._print_tasks_recursive()

        for i, task in enumerate(self.curr.subtasks, 1):
            if task.subtasks:
                print(f"{i}. {task.name} ►")
            else:
                print(f"{i}. {task.name}")
            
            task_ids.add(str(i))
        
        return task_ids

    def _print_tasks_recursive(self, task: TaskNode = None, path: list[str] = []) -> set[str]:
        """
        Recursively prints the subtasks of the current task or optionally a specified task.

        Returns a set of the tasks' ids.
        """
        task_ids = set()
        task = task if task else self.curr
        for i, subtask in enumerate(task.subtasks, 1):
            task_id = ".".join(path + [str(i)])
            spacer = " │  " * len(path)
            if subtask.subtasks:
                print(f"{spacer} {task_id}. {subtask.name} ►")
                task_ids.update(self._print_tasks_recursive(subtask, path + [str(i)]))
            else:
                print(f"{spacer} {task_id}. {subtask.name}")
            
            task_ids.add(task_id)
        
        return task_ids
    
    def get_leaves(self, task: TaskNode = None) -> list[TaskNode]:
        """
        Returns a list of the leaf tasks of the current task or optionally a specified task.
        """
        task = task if task else self.curr
        leaves = []
        for subtask in task.subtasks:
            if subtask.subtasks:
                leaves.extend(self.get_leaves(subtask))
            else:
                leaves.append(subtask)
        
        return leaves
    
    def get_path(self, task: TaskNode = None) -> Iterator[str]:
        """
        Returns an iterator for the path to the current task or optionally a specified task.
        """
        path = []
        if task and not task.parent:
            return path

        curr = task.parent if task is not None else self.curr
        while curr.parent:
            path.append(curr.name)
            curr = curr.parent

        return reversed(path)
    
    def path_str(self, task: TaskNode = None) -> str:
        """
        Returns the path to the current task or optionally a specified task as a string.
        """
        res = " ► ".join(self.get_path(task))
        if res: res += " ►"
        return res

    def __len__(self):
        """
        Returns the number of subtasks of the current task.
        """
        return len(self.curr)
    
    def __iter__(self):
        """
        Iterates through the subtasks of the current task.
        """
        yield from self.curr

    def __getitem__(self, index: int) -> TaskNode:
        """
        Returns the subtask at the specified index.
        """
        return self.curr[index]

    def as_JSON_object(self) -> dict:
        return self.root.as_JSON_object()


if __name__ == "__main__":
    x = TaskTree()
    x.add_tasks(["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"])
    x.into("4")
    x.add_tasks(["Task 4.1", "Task 4.2"])
    x.into("2")
    x.add_tasks(["Task 4.2.1", "Task 4.2.2", "Task 4.2.3"])

    x.back()
    x.back()

    print([x.name for x in x.get_leaves()])