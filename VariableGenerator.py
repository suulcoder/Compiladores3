from Node import Node
from NodeType import NodeType

class VariableGenerator:
    def __init__(self, word_, identities):
        self.current_word_index = 0
        self.word = word_
        self.identities = identities
        self.current_node = None
        self.previous_node = None
        self.value = None
        self.current_word = word_
        self.getNext()

    def getNext(self):
        if type(self.word) != list:
            return
        if(self.current_word_index < len(self.word)):
            self.previous_node = self.current_node
            self.current_node = self.word[self.current_word_index]
            self.current_word_index += 1
        else:
            self.current_node = None
            
        if self.value:
            pass
        else:
            self.value = self.current_node.value

    def generateVariable(self):
        while self.current_node != None:
            if self.current_node.type == NodeType["UNION"]:
                self.getVariable('UNION')
                self.getNext()
            elif self.current_node.type == NodeType["RANGE"]:
                self.getRange()
                self.getNext()
            elif self.current_node.type == NodeType["SUBSTRACTION"]:
                self.getVariable('DIFFERENCE')
                self.getNext()
            else:
                self.getNext()
        return self.value

    def getVariable(self, op):
        self.getNext()
        if(self.current_node):
            curr_word = self.current_node.value
            if op == 'UNION':
                self.value = self.value.union(curr_word)
            elif op == 'DIFFERENCE':
                self.value = self.value.difference(curr_word)

    def getRange(self):
        previous_character = self.previous_node
        self.getNext()
        new_character = self.current_node

        if new_character.type != NodeType["CHAR"] or previous_character.type != NodeType["CHAR"]:
            raise Exception('Range is invalid')
        previous_range = ord(previous_character.value.pop())
        new_range = ord(new_character.value.pop())

        if previous_range > new_range:
            previous_range, new_range = new_range, previous_range
        char_range = set([chr(char)
                          for char in range(previous_range, new_range + 1)])

        self.value.update(char_range)