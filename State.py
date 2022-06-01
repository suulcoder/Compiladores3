import itertools

class State():
    new_id = itertools.count()
    def __init__(self, clousure=None):
        super(State, self).__init__()
        self.id = next(State.new_id)
        self.marked = False
        self.clousure = clousure
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, State):
            return self.id == other.id
        return False
    
    def mark(self):
        self.marked = True
        
    def unmark(self):
        self.marked = False
        
    def __hash__(self):
        return hash(self.id)
        
        