
class Goal:

    def set(self, goal):

        self.goal = goal
        self.completed = False
        self.subgoals = []
    
    def add_subgoal(self, subgoal):

        self.subgoals.append(Goal(subgoal))
