
class TaskManager:

    def set(self):

        self.tasks = []
        self.undo_stack = []

    def add(self, task):

        self.tasks.append({"task": task, "done": False})
    
    def complete(self, index):

        self.tasks[index]["done"] = True

    def undo(self):

        if self.tasks:

            last = self.tasks.pop()
            self.undo_stack.append()

    def redo(self):

        if self.undo_stack:

            self.tasks.append(self.undo_stack.pop())


