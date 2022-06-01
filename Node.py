"""
    This object represents a Node, 
"""
class Node:
    def __init__(self, type, value=None, name=None):
        self.type = type        #Must be a VarType
        self.value = value      #dynamic type
        self.name = name        #Must be a string
        