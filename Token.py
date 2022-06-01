"""
    This object represents a Token, 
"""
import codecs
from Node import Node
from NodeType import NodeType
from modules import getType


class Token:
    def __init__(self, ident, value, context=None):
        self.ident = ident
        self.value = value
        self.context = context
        
class ExecuteToken:
    def __init__(self, word_, identities):
        self.ignore_symbols = ['|','(', '[', '{',]
        self.closing_symbols = ['(','[','{',]
        self.current_character = None
        self.previous_character = None
        self.last_character = None
        self.identities = identities
        self.current_word_index = 0
        self.current_word = word_[self.current_word_index]
        self.word = word_
        self.current_word = word_
        self.getNext()

    def getNext(self):
        if self.current_character == ' ' and self.previous_character == '|':
            self.last_character = self.previous_character
            self.previous_character = '.'
        else:
            self.last_character = self.previous_character
            self.previous_character = self.current_character

        if(self.current_word_index < len(self.current_word)):
            self.current_character = self.word[self.current_word_index]
        else:
            self.current_character = None
        self.current_word_index += 1

    def parse(self, token_id=None):
        while self.current_character != None:
            if self.current_character.isalpha():
                if (self.previous_character and 
                        self.last_character not in self.ignore_symbols and 
                        self.previous_character not in self.ignore_symbols):
                    yield Node(NodeType["CONCATENATION"])
                yield self.generateWord()
            elif self.current_character == '|':
                self.getNext()
                yield Node(NodeType["OR"])
            elif self.current_character == '}':
                self.getNext()
                yield Node(NodeType["RIGHT_KLEENE"])
            elif self.current_character == ']':
                self.getNext()
                yield Node(NodeType["RIGHT_BRACKET"])
            elif self.current_character == ')':
                self.getNext()
                yield Node(NodeType["RIGHT_PARENTHESIS"])
            elif self.current_character in self.closing_symbols:
                if (self.previous_character and  
                        self.last_character not in self.ignore_symbols and
                        self.previous_character not in self.ignore_symbols):
                    yield Node(NodeType["CONCATENATION"])
                if self.current_character == '{':
                    yield Node(NodeType["LEFT_KLEENE"])
                elif self.current_character == '[':
                    yield Node(NodeType["LEFT_BRACKET"])
                elif self.current_character == '(':
                    yield Node(NodeType["LEFT_PARENTHESIS"])
                self.getNext()
            elif self.current_character == '\'' or self.current_character == '"':
                if (self.previous_character and  
                        self.last_character not in self.ignore_symbols and
                        self.previous_character not in self.ignore_symbols):
                    yield Node(NodeType["CONCATENATION"])
                for node in self.generateNode(self.current_character):
                    yield node
            elif self.current_character == ' ':
                self.getNext()
                continue
            else:
                raise Exception(self.current_character + ' Invalid Character!')
        if token_id != None:
            yield Node(NodeType["CONCATENATION"], '.')
            yield Node(NodeType["STRING"], f'#-{token_id}')

    def generateWord(self):
        word = self.current_character
        self.getNext()
        while (self.current_character != None and 
               self.current_character.isalnum() and self.current_character != ' '):
            word += self.current_character
            self.getNext()
        if getType(word, self.identities):
            return getType(word, self.identities)

    def generateNode(self, type):
        node = self.current_character
        self.getNext()
        while self.current_character != None:
            node += self.current_character
            self.getNext()
            if self.current_character == type:
                node += self.current_character
                self.getNext()
                break

        if node.count(type) != 2:
            raise Exception(f'Expected {type} for set')

        node = node.replace(type, '')
        if type == '\'':
            try:
                char = codecs.decode(node, 'unicode_escape')
                ord_ = ord(char)
                return [Node(NodeType["CHAR"], set(chr(ord_)))]
            except:
                raise Exception('invalid char in ' + node)
        elif type == '\"':
            toReturn = []
            for char in node:
                toReturn.append(Node(NodeType["STRING"], set(char)))
                toReturn.append(Node(NodeType["CONCATENATION"], '.'))
            if self.last_character not in self.closing_symbols:
                toReturn.pop()
            return toReturn

