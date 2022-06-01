from math import inf

from enum import Enum
from dataclasses import dataclass

from pprint import pprint

import codecs

import codecs
import pickle
from re import findall

CONTEXT_WORDS = ['ANY']
ANY_SET = set([chr(char) for char in range(0, 256)])


def GetTextInsideSymbols(string, init_symbol, end_symbol):
    start = string.find(init_symbol)
    end = string.find(end_symbol)

    if start == -1 or end == -1:
        return None

    if string.count(init_symbol) != 1 or string.count(end_symbol) != 1:
        return None

    return string[start+1:end]


def GetTextFromDoubleQuotes(string):
    text = findall('"([^"]*)"', string)

    if not text:
        return None
    if len(text) > 1:
        return None

    return text[0]


def GetTextFromSingleQuotes(string):
    text = findall("'([^']*)'", string)

    if not text:
        return None
    if len(text) > 1:
        return None

    return str(text[0])


def GetNoAlpha(string):
    pos = 1
    while pos < len(string) and (string[pos].isalpha() or string[pos] == '|'):
        pos += 1
    return pos if pos < len(string) else None


def IdentExists(ident, char_set):
    try:
        next(filter(lambda x: x.ident == ident, char_set))
        return True
    except StopIteration:
        return False


def GetIdentValue(ident, char_set):
    try:
        ident = next(filter(lambda x: x.ident == ident, char_set))
        return ident.value
    except StopIteration:
        return None


def GetCharValue(char):
    # Finally, we check for the text inside the parenthesis
    value = GetTextInsideSymbols(char, '(', ')')

    # Check for missing or extra parenthesis
    if value == None:
        raise Exception(
            'In CHARACTERS, char is not defined correctly: missplaced parenthesis')

    # Check if the value is a digit
    if not value.isdigit():
        raise Exception(
            'In CHARACTERS, char is not defined correctly: non-digit CHR value')

    return chr(int(value))


def GetElementType(string, char_set):

    if string.count('"') == 2:
        string = string.replace('\"', '')
        val = set([chr(ord(char)) for char in string])
        return Variable(VarType.STRING, val)

    if string.count('\'') == 2:
        char = GetTextFromSingleQuotes(string)
        try:
            char = codecs.decode(char, 'unicode_escape')
            ord_ = ord(char)
        except:
            raise Exception(f'Unvalid char in GetElementType: {string}')

        new_set = set(chr(ord_))
        return Variable(VarType.CHAR, new_set)

    if string in CONTEXT_WORDS:
        if 'ANY' == string:
            return Variable(VarType.STRING, ANY_SET)

    if string.isdigit():
        return Variable(VarType.NUMBER, string)

    if IdentExists(string, char_set):
        return Variable(VarType.IDENT, GetIdentValue(string, char_set), string)

    if 'CHR' in string:
        char = set(GetCharValue(string))
        return Variable(VarType.CHAR, char)


def WriteToFile(filename: str, content: str):
    with open(filename, 'w') as _file:
        _file.write(content)

    return f'File "{filename}" created!'


def DumpAutomata(automata):
    pickle.dump(automata, open('./output/automata.p', 'wb'))



class TokenExpression:
    def __init__(self, set_, idents):
        self.set = iter(set_)
        self.idents = idents
        self.curr_char = None
        self.prev_char = None
        self.last_char = None
        self.symbol_ignore = ['(', '[', '{', '|']
        self.closing_symbols = ['{', '(', '[']
        self.curr_set = set_
        self.Next()

    def Next(self):
        try:
            if self.curr_char == ' ' and self.prev_char == '|':
                self.last_char = self.prev_char
                self.prev_char = '.'
            else:
                self.last_char = self.prev_char
                self.prev_char = self.curr_char

            self.curr_char = next(self.set)
        except StopIteration:
            self.curr_char = None

    def Parse(self, token_id=None):
        while self.curr_char != None:

            # curr_char is a letter
            if self.curr_char.isalpha():
                if self.prev_char and \
                        self.prev_char not in self.symbol_ignore and \
                        self.last_char not in self.symbol_ignore:

                    yield Variable(VarType.APPEND)
                yield self.GenerateWord()

            # curr_char is a char or string
            elif self.curr_char == '\'' or self.curr_char == '"':
                if self.prev_char and \
                        self.prev_char not in self.symbol_ignore and \
                        self.last_char not in self.symbol_ignore:

                    yield Variable(VarType.APPEND)
                res = self.GenerateVar(self.curr_char)
                for var in res:
                    yield var

            # curr_char is a closing symbol
            elif self.curr_char in self.closing_symbols:
                if self.prev_char and \
                        self.prev_char not in self.symbol_ignore and \
                        self.last_char not in self.symbol_ignore:

                    yield Variable(VarType.APPEND)

                if self.curr_char == '{':
                    yield Variable(VarType.LKLEENE)
                elif self.curr_char == '[':
                    yield Variable(VarType.LBRACKET)
                elif self.curr_char == '(':
                    yield Variable(VarType.LPAR)

                self.Next()

            # curr_char is kleene expr.
            elif self.curr_char == '}':
                self.Next()
                yield Variable(VarType.RKLEENE)

            elif self.curr_char == ']':
                self.Next()
                yield Variable(VarType.RBRACKET)

            elif self.curr_char == ')':
                self.Next()
                yield Variable(VarType.RPAR)

            elif self.curr_char == '|':
                self.Next()
                yield Variable(VarType.OR)

            elif self.curr_char == ' ':
                self.Next()
                continue

            else:
                raise Exception(f'Invalid character: {self.curr_char}')

        if token_id != None:
            yield Variable(VarType.APPEND, '.')
            yield Variable(VarType.STRING, f'#-{token_id}')

    def GenerateWord(self):
        word = self.curr_char
        self.Next()

        while self.curr_char != None \
                and self.curr_char.isalnum() and self.curr_char != ' ':
            word += self.curr_char
            self.Next()

        res = GetElementType(word, self.idents)
        if not res:
            raise Exception(
                f'Invalid ident: {word} in expression "{self.curr_set}"')

        return res

    def GenerateVar(self, symbol_type):
        var = self.curr_char
        self.Next()

        while self.curr_char != None:
            var += self.curr_char
            self.Next()

            if self.curr_char == symbol_type:
                var += self.curr_char
                self.Next()
                break

        if var.count(symbol_type) != 2:
            raise Exception(f'Expected {symbol_type} for set')

        var = var.replace(symbol_type, '')
        if symbol_type == '\'':
            try:
                char = codecs.decode(var, 'unicode_escape')
                ord_ = ord(char)
            except:
                raise Exception(f'Unvalid char in Generate var: {var}')

            return [Variable(VarType.CHAR, set(chr(ord_)))]

        elif symbol_type == '\"':
            res = list()
            for char in var:
                res.append(Variable(VarType.STRING, set(char)))
                res.append(Variable(VarType.APPEND, '.'))

            if self.last_char not in self.closing_symbols:
                res.pop()
            return res


class SetDecl:
    def __init__(self, set_, idents):
        self.set = iter(set_)
        self.idents = idents
        self.curr_char = None
        self.curr_set = set_
        self.valid_alnum = ['(', ')']
        self.Next()

    def Next(self):
        try:
            self.curr_char = next(self.set)
        except StopIteration:
            self.curr_char = None

    def Set(self):
        while self.curr_char != None:

            # curr_char is a letter
            if self.curr_char.isalpha():
                yield self.GenerateWord()

            # curr_char is a char or string
            elif self.curr_char == '\'' or self.curr_char == '"':
                yield self.GenerateVar(self.curr_char)

            elif self.curr_char == '+':
                self.Next()
                yield Variable(VarType.UNION)

            elif self.curr_char == '-':
                self.Next()
                yield Variable(VarType.DIFFERENCE)

            elif self.curr_char == '.':
                self.Next()
                if self.curr_char == '.':
                    self.Next()
                    yield Variable(VarType.RANGE)
                else:
                    raise Exception(
                        f'Invalid dot found in set: {self.curr_set}')

            elif self.curr_char == ' ':
                self.Next()

    def GenerateWord(self):
        word = self.curr_char
        self.Next()

        while self.curr_char != None \
                and (self.curr_char.isalnum() or self.curr_char in self.valid_alnum) \
                and self.curr_char != ' ':
            word += self.curr_char
            self.Next()

        if 'CHR(' in word:
            res = GetCharValue(word)
            res = Variable(VarType.CHAR, set(res))
        else:
            res = GetElementType(word, self.idents)

        if not res:
            raise Exception(
                f'Invalid ident: {word} in expression "{self.curr_set}"')

        return res

    def GenerateVar(self, symbol_type):
        var = self.curr_char
        self.Next()

        while self.curr_char != None:
            var += self.curr_char
            self.Next()

            if self.curr_char == symbol_type:
                var += self.curr_char
                self.Next()
                break

        if var.count(symbol_type) != 2:
            raise Exception(f'Expected {symbol_type} for set')

        res = GetElementType(var, self.idents)

        if not res:
            raise Exception(f'Invalid var: {var}')

        return res


class SetGenerator:
    def __init__(self, set_, idents):
        self.set = iter(set_)
        self.idents = idents
        self.curr_var = None
        self.prev_var = None
        self.res_set = None
        self.curr_set = set_
        self.Next()

    def Next(self):
        try:
            self.prev_var = self.curr_var
            self.curr_var = next(self.set)
        except StopIteration:
            self.curr_var = None

        if not self.res_set:
            self.res_set = self.curr_var.value

    def GenerateSet(self):
        while self.curr_var != None:

            if self.curr_var.type == VarType.UNION:
                self.NewSet('UNION')
                self.Next()

            elif self.curr_var.type == VarType.DIFFERENCE:
                self.NewSet('DIFFERENCE')
                self.Next()

            elif self.curr_var.type == VarType.RANGE:
                self.NewRange()
                self.Next()

            else:
                self.Next()

        return self.res_set

    def NewSet(self, op):
        self.Next()

        if self.curr_var.value == None:
            Exception(f'Unvalid set declaration')

        curr_set = self.curr_var.value

        if op == 'UNION':
            self.res_set = self.res_set.union(curr_set)
        elif op == 'DIFFERENCE':
            self.res_set = self.res_set.difference(curr_set)

    def NewRange(self):
        char1 = self.prev_var
        self.Next()
        char2 = self.curr_var

        if char1.type != VarType.CHAR or char2.type != VarType.CHAR:
            raise Exception(
                f'Unvalid char range found in {self.curr_set}')

        # We gotta .pop since the value is a set of 1 item
        range1 = ord(char1.value.pop())
        range2 = ord(char2.value.pop())

        if range1 > range2:
            range1, range2 = range2, range1

        # Create a new list with all the chars in the range
        char_range = set([chr(char)
                          for char in range(range1, range2 + 1)])

        self.res_set.update(char_range)


class Parser:
    def __init__(self, cfg):
        self.cfg = cfg
        self.tokens = None
        self.parsed_tree = list()

    def Next(self):
        try:
            self.curr_token = next(self.tokens)
        except StopIteration:
            self.curr_token = None

    def NewSymbol(self):
        token = self.curr_token

        if token.type == VarType.LPAR:
            self.Next()
            res = self.Expression()

            if self.curr_token.type != VarType.RPAR:
                raise Exception('No right parenthesis for expression!')

            self.Next()
            return res

        elif token.type == VarType.CHAR or token.type == VarType.IDENT or token.type == VarType.STRING:
            self.Next()
            if token.type == VarType.IDENT:
                return Symbol(token.value, token.type, token.name)
            return Symbol(token.value, token.type)

    def NewGroup(self):
        res = self.NewSymbol()

        while self.curr_token != None and \
                (
                    self.curr_token.type == VarType.LKLEENE or
                    self.curr_token.type == VarType.LBRACKET
                ):
            if self.curr_token.type == VarType.LKLEENE:
                self.Next()
                res = Kleene(self.Expression())

                if self.curr_token.type != VarType.RKLEENE:
                    raise Exception('No right curly bracket for a token!')
                self.Next()

            elif self.curr_token.type == VarType.LBRACKET:
                self.Next()
                res = Bracket(self.Expression())

                if self.curr_token.type != VarType.RBRACKET:
                    raise Exception('No right bracket for a token!')
                self.Next()

        return res

    def Term(self):
        res = self.NewGroup()

        while self.curr_token != None and self.curr_token.type == VarType.APPEND:
            self.Next()
            res = Append(res, self.NewGroup())

        return res

    def Expression(self):
        res = self.Term()

        while self.curr_token != None and self.curr_token.type == VarType.OR:
            self.Next()
            res = Or(res, self.Expression())

        return res

    def Parse(self, tokens):
        self.tokens = iter(tokens)
        self.Next()
        if self.curr_token == None:
            return None

        res = self.Expression()
        return res

    def ToSingleExpression(self):
        new_list = list()
        for token in self.cfg.tokens:
            tokens = token.value
            tokens.insert(0, Variable(VarType.LPAR, '('))
            tokens.append(Variable(VarType.RPAR, ')'))
            tokens.append(Variable(VarType.OR, '|'))
            new_list += tokens

        new_list.pop()
        return new_list


RAW_STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


class DFA:
    def __init__(self, tree, symbols, keywords, ignore_set):

        # Useful for syntax tree
        self.nodes = list()

        # FA properties
        self.symbols = symbols
        self.states = list()
        self.trans_func = dict()
        self.accepting_states = set()
        self.accepting_dict = dict()
        self.initial_state = 'A'
        self.keywords = keywords
        self.keywords_value = [
            keyword.value.value for keyword in self.keywords]
        self.ignore_set = ignore_set

        # Class properties
        self.tree = tree
        self.augmented_states = None
        self.iter = 1

        self.STATES = iter(RAW_STATES)

        # Initialize dfa construction
        self.ParseTree(self.tree)
        self.CalcFollowPos()

    def CalcFollowPos(self):
        for node in self.nodes:
            if node.value == '*':
                for i in node.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.firstpos
            elif node.value == '.':
                for i in node.c1.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.c2.firstpos

        # Initiate state generation
        initial_state = self.nodes[-1].firstpos

        # Filter the nodes that have a symbol
        self.nodes = list(filter(lambda x: x._id, self.nodes))

        # Get all the nodes with the symbol '#'.
        self.augmented_states = list(
            filter(lambda x: '#-' in x.value, self.nodes))

        self.augmented_states = set(
            [node._id for node in self.augmented_states])

        # Recursion
        self.CalcNewStates(initial_state, next(self.STATES))

    def CalcNewStates(self, state, curr_state):

        if not self.states:
            self.states.append(set(state))

            # If state in set(self.augmented_states).
            if state in list(self.augmented_states):
                self.accepting_dict[curr_state] = state
                self.accepting_states.update(curr_state)

        # Iteramos por cada símbolo
        for symbol in self.symbols:

            # Get all the nodes with the same symbol in followpos
            same_symbols = list(
                filter(lambda x: symbol in x.value and x._id in state, self.nodes))

            # Create a new state with the nodes
            new_state = set()
            for node in same_symbols:
                new_state.update(node.followpos)

            # new state is not in the state list
            if new_state not in self.states and new_state:

                # Get this new state's letter
                self.states.append(new_state)
                next_state = next(self.STATES)

                # Add state to transition function
                try:
                    self.trans_func[next_state]
                except:
                    self.trans_func[next_state] = dict()

                try:
                    existing_states = self.trans_func[curr_state]
                except:
                    self.trans_func[curr_state] = dict()
                    existing_states = self.trans_func[curr_state]

                # Add the reference
                existing_states[symbol] = next_state
                self.trans_func[curr_state] = existing_states

                # Is it an accepting_state?
                if bool(self.augmented_states & new_state):
                    self.accepting_states.update(next_state)
                    self.accepting_dict[next_state] = new_state

                # Repeat with this new state
                self.CalcNewStates(new_state, next_state)

            elif new_state:
                # State already exists... which one is it?
                for i in range(0, len(self.states)):

                    if self.states[i] == new_state:
                        state_ref = RAW_STATES[i]
                        break

                # Add the symbol transition
                try:
                    existing_states = self.trans_func[curr_state]
                except:
                    self.trans_func[curr_state] = {}
                    existing_states = self.trans_func[curr_state]

                existing_states[symbol] = state_ref
                self.trans_func[curr_state] = existing_states

    def ParseTree(self, node):
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def SymbolNode(self, node):
        new_node = Node(self.iter, [self.iter], [self.iter],
                        value=node.value, nullable=False)
        self.nodes.append(new_node)
        return new_node

    def OrNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.lastpos + node_b.lastpos

        new_node = Node(None, firstpos, lastpos,
                        is_nullable, '|', node_a, node_b)

        self.nodes.append(new_node)
        return new_node

    def AppendNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable and node_b.nullable
        if node_a.nullable:
            firstpos = node_a.firstpos + node_b.firstpos
        else:
            firstpos = node_a.firstpos

        if node_b.nullable:
            lastpos = node_b.lastpos + node_a.lastpos
        else:
            lastpos = node_b.lastpos

        new_node = Node(None, firstpos, lastpos,
                        is_nullable, '.', node_a, node_b)

        self.nodes.append(new_node)
        return new_node

    def KleeneNode(self, node):
        node_a = self.ParseTree(node.a)
        firstpos = node_a.firstpos
        lastpos = node_a.lastpos
        new_node = Node(None, firstpos, lastpos, True, '*', node_a)
        self.nodes.append(new_node)
        return new_node

    def BracketNode(self, node):
        # Node_a is epsilon
        node_a = Node(None, list(), list(), True)
        # self.iter += 1
        node_b = self.ParseTree(node.a)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.lastpos + node_b.lastpos

        new_node = Node(None, firstpos, lastpos,
                        is_nullable, '|', node_a, node_b)
        self.nodes.append(new_node)
        return new_node

class Node:
    def __init__(self, _id, firstpos=None, lastpos=None, nullable=False, value=None, c1=None, c2=None):
        self._id = _id
        self.firstpos = firstpos
        self.lastpos = lastpos
        self.followpos = list()
        self.nullable = nullable
        self.value = value
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return f'''
    id: {self._id}
    value: {self.value}
    firstpos: {self.firstpos}
    lastpos: {self.lastpos}
    followpos: {self.followpos}
    nullabe: {self.nullable}
    '''



# __________IMPORTANT DATA CLASSES__________
class Element:
    def __init__(self, ident, value):
        self.ident = ident
        self.value = value

    def __repr__(self):
        return f'{self.ident} = {self.value}'


class Character(Element):
    def __init__(self, ident, value):
        super().__init__(ident, value)


class Keyword(Element):
    def __init__(self, ident, value):
        super().__init__(ident, value)


class Token(Element):
    def __init__(self, ident, value, context=None):
        super().__init__(ident, value)
        self.context = context

    def __repr__(self):
        if self.context != None:
            return f'{self.ident} = {self.value} {self.context}'
        return f'{self.ident} = {self.value}'


# __________ALL THE DIFFERENT SYMBOLS__________
class VarType(Enum):
    IDENT = 0
    STRING = 1
    CHAR = 2
    NUMBER = 3
    UNION = 4
    DIFFERENCE = 5
    RANGE = 6
    APPEND = 7
    LKLEENE = 8
    RKLEENE = 9
    LPAR = 10
    RPAR = 11
    LBRACKET = 12
    RBRACKET = 13
    OR = 14


@dataclass
class Variable:
    type: VarType
    value: any = None
    name: str = None

    def __repr__(self):
        if self.name:
            return f'{self.type.name}: {self.name}'
        return self.type.name + (f':{self.value}' if self.value != None else '')


# __________NODE TYPES__________
class Kleene:
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return '{ ' + f'{self.a}' + ' }'


class Bracket:
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f'[ {self.a} ]'


class Or:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a}) | ({self.b})'
        # return f'{self.a} | {self.b}'


class Append:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        # return f'({self.a} . {self.b})'
        return f'{self.a} . {self.b}'


class Symbol:
    def __init__(self, value, type_=None, ident_name=None):
        self.value = value
        self.type = type_
        self.ident_name = ident_name

    def __repr__(self):
        if self.ident_name:
            return f'{self.ident_name}'
        return f'{self.value}'


SCANNER_WORDS = ['COMPILER', 'CHARACTERS', 'IGNORE',
                 'KEYWORDS', 'TOKENS', 'END', 'PRODUCTIONS']


class Lexer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None

        self.compiler_name = None
        self.characters = list()
        self.keywords = list()
        self.tokens = list()
        self.ignore = set()

        self.file_lines = self.ReadFile()
        self.curr_line = None
        self.Next()

        self.ReadLines()
        self.allchars = set()

    def Next(self):
        try:
            self.curr_line = next(self.file_lines)
        except StopIteration:
            self.curr_line = None

    def ReadFile(self):
        try:
            self.file = open(self.filepath, 'r', encoding='latin-1')
        except:
            raise Exception('File not found!')
        finally:
            lines = self.file.readlines()
            temp = list()
            for line in lines:
                if line != '\n':
                    line = line.strip('\r\t\n')
                    line = line.strip()
                    line = line.split(' ')
                    line[:] = [i for i in line if i != '' or i]
                    temp.append(line)

        return iter(temp)

    def ReadLines(self):
        while self.curr_line != None:
            # Check if we got any important word in the lines
            if any(word in SCANNER_WORDS for word in self.curr_line):

                if 'COMPILER' in self.curr_line:
                    self.compiler_name = self.curr_line[self.curr_line.index(
                        'COMPILER')+1]
                    self.Next()

                elif 'CHARACTERS' in self.curr_line:
                    self.Next()
                    self.ReadSection('CHARACTERS')

                elif 'KEYWORDS' in self.curr_line:
                    self.Next()
                    self.ReadSection('KEYWORDS')

                elif 'TOKENS' in self.curr_line:
                    self.Next()
                    # print('\n', '='*20, 'TOKENS', '='*20)
                    self.ReadSection('TOKENS')

                elif 'IGNORE' in self.curr_line:
                    self.ReadIgnore()
                    self.Next()

                elif 'PRODUCTIONS' in self.curr_line:
                    self.Next()

                elif 'END' in self.curr_line:
                    end_compiler_name = self.curr_line[self.curr_line.index(
                        'END')+1]
                    self.Next()

            elif '(.' in self.curr_line[:2]:
                self.ReadComment()
                self.Next()

            else:
                self.Next()

    def ReadSection(self, section):
        joined_set = ''
        while not any(word in SCANNER_WORDS for word in self.curr_line):
            curr_set = ' '.join(self.curr_line)

            # Is there a comment?
            if '(.' in curr_set[:2]:
                self.ReadComment()

            # Does the set contains both = and .
            if '=' in curr_set and '.' == curr_set[-1] and joined_set != '':
                curr_set = curr_set[:-1]
                self.GetKeyValue(curr_set, section)
                self.Next()

            # elif '=' in curr_set and not '.' == curr_set[-1]:
            #     print('\nWARNING: Statement without ending (Ignored):', curr_set)
            #     self.Next()

            # If it doesn't contains a ., it's probably part of the previous set
            elif not '.' == curr_set[-1]:
                joined_set += curr_set
                self.Next()

            # If there's a ., it's probably the end of a previously joined set
            elif '.' == curr_set[-1]:
                joined_set += curr_set
                joined_set = joined_set[:-1]
                self.GetKeyValue(joined_set, section)
                self.Next()

            elif '(.' in self.curr_line:
                self.ReadComment()
                self.Next()

            else:
                print('WARNING: Ignored statement:', curr_set)
                self.Next()

    def ReadComment(self):
        while not '.)' in self.curr_line:
            self.Next()

    def ReadIgnore(self):
        curr_set = ' '.join(self.curr_line)
        line = curr_set.split('IGNORE', 1)[1]
        line = line.replace('.', '')

        value = SetDecl(line, self.characters).Set()
        final_set = SetGenerator(value, self.characters).GenerateSet()
        self.ignore = final_set

    def GetKeyValue(self, line, attr):
        if attr == 'CHARACTERS':
            self.SetDecl(line)
        elif attr == 'KEYWORDS':
            self.KeywordDecl(line)
        elif attr == 'TOKENS':
            self.TokenDecl(line)

    def TokenDecl(self, line):
        ident, value = line.split('=', 1)
        ident = ident.strip()
        value = value.strip()
        context = None

        # Check if ident exists
        if IdentExists(ident, self.characters):
            raise Exception(f'Ident "{ident}" declared twice!')

        # Are there any keywords?
        # TODO: Except might be lower case or upper case
        if 'EXCEPT' in value:
            kwd_index = value.index('EXCEPT')
            context = value[kwd_index:]
            value = value[:kwd_index]

        # Parse this new set
        parser = TokenExpression(value, self.characters)
        value = parser.Parse(token_id=ident)
        token = Token(ident, list(value), context)
        # print()
        # print(f'{token}')
        self.tokens.append(token)

    def KeywordDecl(self, line):
        ident, value = line.split('=', 1)
        ident = ident.strip()
        value = value.strip().replace('.', '')
        value = value.replace('"', '')
        value = Variable(VarType.STRING, value)

        # Create ident object
        keyword = Keyword(ident, value)

        # Check if ident exists, else append it to list
        if IdentExists(ident, self.keywords):
            raise Exception('Keyword declared twice!')

        self.keywords.append(keyword)

    def SetDecl(self, line):
        key, value = line.split('=', 1)

        key = key.strip()
        set_decl = SetDecl(value, self.characters)
        value = list(set_decl.Set())
        # print()
        # print(f'CRUDO:\n{key}: {value}')
        final_set = SetGenerator(value, self.characters).GenerateSet()
        # print()
        # print(f'GENERADO\n{key}: {final_set}')
        self.characters.append(Character(key, final_set))

    def GenerateSet(self, eval_set):
        generator = SetGenerator(eval_set, self.characters)
        generated_set = generator.GenerateSet()
        return generated_set

    def GetAllChars(self):
        for character in self.characters:
            self.allchars.update(character.value)
        for token in self.tokens:
            for var in token.value:
                if var.type == VarType.CHAR or var.type == VarType.STRING:
                    self.allchars.update(var.value)

        return self.allchars

    def __repr__(self):
        return f'''
Compiler: {self.compiler_name}

Characters:
{self.characters}

Keywords:
{self.keywords}

Tokens:
{self.tokens}

''' + (f'Ignore: {self.ignore}' if self.ignore else '')



# from Token import ExecuteToken
# from Variable import Variable
# from VariableGenerator import VariableGenerator
# from NodeType import NodeType
# from Character import Character
# from Keyword import Keyword
# from Token import Token
# from Node import Node

# COCO_RESERVED_WORDS = [
#      'CHARACTERS',
#      'COMPILER',
#      'END',
#      'IGNORE',
#      'KEYWORDS', 
#      'PRODUCTIONS',
#      'TOKENS']


# class Lexer:
#     def __init__(self, filepath):
#         self.compiler_name = None
#         self.current_index = 0
#         self.characters = []
#         self.keywords = []
#         self.tokens = []
#         self.ignore = []

#         self.read(filepath)
#         self.getNextLine()

#         self.processLines()
#         self._characters = set()
        
#     def getCharacters(self):
#         for character in self.characters:
#             self._characters.update(character.value)
#         for token in self.tokens:
#             for node in token.value:
#                 if node.type == NodeType["CHAR"] or node.type == NodeType["STRING"]:
#                     self._characters.update(node.value)

#         return self._characters

#     #This file is useful to get the data from the file
#     def read(self, filepath):
#         lines = []
#         for line in open(filepath, 'r').readlines():
#             if line == '\n':
#                 pass
#             else:
#                 #Add all the characters to a single string, 
#                 #Ignoring uneuseful characeters
#                 lines.append(
#                     [character for character in 
#                      line.strip().strip('\r\t\n').split(' ') 
#                      if character != '' or character]
#                 )
#         #Update lines
#         self.lines =  lines

#     #Get the next line
#     def getNextLine(self):
#         if(self.current_index  < len(self.lines)):
#             self.current_line = self.lines[self.current_index]
#             self.current_index += 1
#         else:
#             self.current_line = None

#     #Get all tokens from the lines
#     def processLines(self):
#         #While there is a new line
#         while self.current_line != None:
#             #If compiler is in the line
#             if 'COMPILER' in self.current_line:
#                 #We have the compiler name
#                 self.compiler_name = self.current_line[self.current_line.index(
#                     'COMPILER')+1]
#                 self.getNextLine()
#             #If ignore is in the line
#             elif 'IGNORE' in self.current_line:
#                 #We generate a set of variables that we will ignore and delete
#                 self.ignore = VariableGenerator(
#                     Variable(' '.join(self.current_line).split('IGNORE', 1)[1].replace('.', ''), self.characters).parse_variable(),
#                     self.characters
#                     ).generateVariable()
#                 self.getNextLine()
#             elif 'KEYWORDS' in self.current_line:
#                 self.getNextLine()
#                 self.readLine('KEYWORDS')
#             elif 'CHARACTERS' in self.current_line:
#                 self.getNextLine()
#                 self.readLine('CHARACTERS')
#             elif 'TOKENS' in self.current_line:
#                 self.getNextLine()
#                 self.readLine('TOKENS')
#             elif '(.' in self.current_line[:2]:
#                 self.readComment()
#                 self.getNextLine()
#             else:
#                 self.getNextLine()

#     def readComment(self):
#         while not '.)' in self.current_line:
#             self.getNextLine()

#     def readLine(self, cocoWord):
#         temporal_token = ''
#         has_reserved_words = False
#         for word in self.current_line:
#             has_reserved_words = has_reserved_words or word in COCO_RESERVED_WORDS
#         while not has_reserved_words:
#             current_set = ' '.join(self.current_line)
#             if '(.' in self.current_line:
#                 self.readComment()
#                 self.getNextLine()
#             elif '.' == current_set[-1] and '=' in current_set  and temporal_token != '':
#                 current_set = current_set[:-1]
#                 if cocoWord == 'KEYWORDS':
#                         self.execute_keywords(current_set)
#                 elif cocoWord == 'CHARACTERS':
#                     self.execute_declarations(current_set)
#                 elif cocoWord == 'TOKENS':
#                     self.execute_tokens(current_set)
#                 self.getNextLine()
#             elif not '.' == current_set[-1]:
#                 temporal_token += current_set
#                 self.getNextLine()
#             elif '.' == current_set[-1]:
#                 temporal_token += current_set
#                 temporal_token = temporal_token[:-1]
#                 if cocoWord == 'KEYWORDS':
#                         self.execute_keywords(temporal_token)
#                 elif cocoWord == 'CHARACTERS':
#                     self.execute_declarations(temporal_token)
#                 elif cocoWord == 'TOKENS':
#                     self.execute_tokens(temporal_token)
#                 self.getNextLine()
#             else:
#                 self.getNextLine()  
#             has_reserved_words = False
#             for word in self.current_line:
#                 has_reserved_words = has_reserved_words or word in COCO_RESERVED_WORDS

#     def GenerateSet(self, eval_set):
#         generator = VariableGenerator(eval_set, self.characters)
#         generated_set = generator.GenerateSet()
#         return generated_set

#     def execute_tokens(self, line):
#         key, value = line.split('=', 1)
#         key = key.strip()
#         value = value.strip()
#         key_content = None

#         if 'EXCEPT' in value:
#             key_index = value.index('EXCEPT')
#             key_content = value[key_index:]
#             value = value[:key_index]
            
#         self.tokens.append(Token(
#             key,
#             list(ExecuteToken(value, self.characters).parse(token_id=key)),
#             key_content))

#     def execute_keywords(self, line):
#         key, value = line.split('=', 1)
#         key = key.strip()
#         value = Node(
#             NodeType["STRING"], value.strip().replace('.', '').replace('"', '')
#             )
#         self.keywords.append(Keyword(key, value))

#     def execute_declarations(self, line):
#         key, value = line.split('=', 1)
#         key = key.strip()
#         self.characters.append(
#             Character(key, 
#                       VariableGenerator(list(Variable(
#                           value, 
#                           self.characters
#                     ).parse_variable()),self.characters).generateVariable()
#                 )
#             )
