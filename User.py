
class User:

    def set(self, username):

        self.username = username
        self.tasks = []
        self.goals = []
        self.notes = []

    def add_task(self, task):

        self.tasks.append(dict(task = task, done = False))
    
    def add_goal(self, goal):

        self.goals.append(dict(goal = goal, done = False ))

    def add_note(self, note):

        self.notes.append(note)

    def show_user(self):

        return "User: " + self.username

    

