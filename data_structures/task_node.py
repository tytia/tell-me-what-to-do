
from dataclasses import dataclass

"""
A tree node with renamed attributes.
"""
@dataclass
class TaskNode:
    name: str
    subtasks: list['TaskNode'] = None
    parent: 'TaskNode' = None

    @classmethod
    def from_JSON_object(cls, data: dict | str) -> 'TaskNode':
        """
        Reconstructs a TaskNode from a JSON object.
        """
        if isinstance(data, str):
            return TaskNode(data)
        
        name = next(iter(data))
        node = TaskNode(name)
        for task in data[name]:
            node.add_child(TaskNode.from_JSON_object(task))
        
        return node

    def add_child(self, task: 'TaskNode') -> None:
        if not self.subtasks:
            self.subtasks = []

        self.subtasks.append(task)
        task.parent = self

    def add_children(self, tasks: list['TaskNode']) -> None:
        for task in tasks:
            self.add_child(task)

    def remove_child(self, index: int) -> 'TaskNode':
        return self.subtasks.pop(index)
    
    def __iter__(self):
        if self.subtasks:
            for task in self.subtasks:
                yield task
                yield from task
        
    def __len__(self):
        res = 0
        for _ in self:
            res += 1
        return res

    def __getitem__(self, index: int) -> 'TaskNode':
        if index < 0:
            raise IndexError("Index out of range")

        i = 0
        for task in self:
            if i == index:
                return task
            i += 1
        
        raise IndexError("Index out of range")

    def as_JSON_object(self) -> dict | str:
        if not self.subtasks:
            return self.name
        
        res = {self.name: []}
        for task in self.subtasks:
            res[self.name].append(task.as_JSON_object())

        return res
    
    def __str__(self):
        return str(self.as_JSON_object())


if __name__ == "__main__":
    x = TaskNode("root", [])
    x.add_children([TaskNode("1"), TaskNode("2"), TaskNode("3"), TaskNode("4"), TaskNode("5")])
    x.subtasks[3].subtasks = []
    x.subtasks[3].add_children([TaskNode("4.1"), TaskNode("4.2")])

    # for item in x:
    #     print(item, end=" ")
    print(x)