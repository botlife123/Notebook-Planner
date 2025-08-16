
#tree structure 
class TaskGraph:

    def set(self):

        self.edges = {}

    def add_task(self, task):

        self.edges.setdefault(task, set())

    def add_dependency(self, task, depends_on):

      self.edges.setdefault(task, set()).add(depends_on)