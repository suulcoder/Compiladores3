class RegexNode:
    def __init__(self, operation, value=None, type_=None, name=None, first_node=None, second_node=None):
        self.value = value
        self.type = type_
        self.ident_name = name
        self.operation = operation
        self.first_node = first_node
        self.second_node = second_node