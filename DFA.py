from Leaf import Leaf
from utils import alphanumeric

class DFA:
    def __init__(self, tree, alphabet, keywords, to_ignore):
        self.final_states = set()
        self.accepting_dictionary = {}
        self.initial_state = alphanumeric[0]
        self.keywords = keywords
        self.keywords_values = [
            keyword.value.value for keyword in self.keywords
            ]
        self.nodes = []
        self.alphabet = alphabet
        self.states = []
        self.transitions = {}
        self.to_ignore = to_ignore if to_ignore!=None else []
        self.tree = tree
        self.augmented_states = None
        self.iteration = 1
        self.STATES = alphanumeric
        self.current_state_index = 0
        self.parse(self.tree)
        self.followPos()
        
    def next_state(self):
        value = self.STATES[self.current_state_index]
        self.current_state_index += 1
        return value

    def followPos(self):
        for node in self.nodes:
            node.getFollowPos(self.nodes)
        initial_state = self.nodes[-1].firstpos
        _nodes = list(filter(lambda x: x._id, self.nodes))
        self.nodes = []
        for n in _nodes:
            if n.value!=None:
                self.nodes.append(n)
        self.augmented_states = set(
            [node._id for node in list(
            filter(lambda node: '#-' in node.value, self.nodes))])
        self.getStates(initial_state, self.next_state())

    def getStates(self, state, current_state):
        if not self.states:
            self.states.append(set(state))
            if state in list(self.augmented_states):
                self.accepting_dictionary[current_state] = state
                self.final_states.update(current_state)
        for character in self.alphabet:
            _state = set()
            for node in list(
                filter(lambda x: character in x.value and x._id in state, self.nodes)):
                _state.update(node.followpos)
            if _state not in self.states and _state:
                self.states.append(_state)
                next_state = self.next_state()
                if next_state not in self.transitions.keys():
                    self.transitions[next_state] = {}
                if current_state not in self.transitions.keys():
                    self.transitions[current_state] = {}    
                self.transitions[current_state][character] = next_state
                self.transitions[current_state] = self.transitions[current_state]
                if bool(self.augmented_states & _state):
                    self.final_states.update(next_state)
                    self.accepting_dictionary[next_state] = _state
                self.getStates(_state, next_state)
            elif _state:
                for index_char in range(0, len(self.states)):
                    if self.states[index_char] == _state:
                        state_ref = alphanumeric[index_char]
                        break
                if current_state not in self.transitions.keys():
                    self.transitions[current_state] = {}
                self.transitions[current_state][character] = state_ref
                self.transitions[current_state] = self.transitions[current_state]

    def parse(self, node):
        if(node.operation=='OR'):
            first_node = self.parse(node.first_node)
            self.iteration += 1
            second_node = self.parse(node.second_node)
            is_nullable = first_node.nullable or second_node.nullable
            toReturn = Leaf(
                None, 
                first_node.firstpos + second_node.firstpos, 
                first_node.lastpos + second_node.lastpos,
                is_nullable, 
                'OR', 
                first_node, 
                second_node)
            self.nodes.append(toReturn)
            return toReturn
        elif(node.operation=='CONCAT'):
            first_node = self.parse(node.first_node)
            self.iteration += 1
            second_node = self.parse(node.second_node)
            toReturn = Leaf(
                None, 
                first_node.firstpos + second_node.firstpos if first_node.nullable else first_node.firstpos, 
                second_node.lastpos + first_node.lastpos if second_node.nullable else second_node.lastpos,
                first_node.nullable and second_node.nullable, 
                'CONCATENATION', 
                first_node, second_node)
            self.nodes.append(toReturn)
            return toReturn
        elif(node.operation=='KLEENE'):
            first_node = self.parse(node.first_node)
            toReturn = Leaf(None, first_node.firstpos, first_node.lastpos, True, 'KLEENE', first_node)
            self.nodes.append(toReturn)
            return toReturn
        elif(node.operation=='PARENTHESIS'):
            first_node = Leaf(None, [], [], True)
            second_node = self.parse(node.first_node)
            toReturn = Leaf(
                None, 
                first_node.firstpos + second_node.firstpos,
                first_node.lastpos + second_node.lastpos,
                first_node.nullable or second_node.nullable,
                'OR',
                first_node, second_node)
            self.nodes.append(toReturn)
            return toReturn
        else:
            toReturn = Leaf(self.iteration, [self.iteration], [self.iteration],
                            value=node.value, nullable=False)
            self.nodes.append(toReturn)
            return toReturn