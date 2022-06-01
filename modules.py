import codecs
from re import findall

from Node import Node
from NodeType import NodeType

def getText(myText):
    if not findall("'([^']*)'", myText):
        return None
    if len(findall("'([^']*)'", myText)) > 1:
        return None
    return str(findall("'([^']*)'", myText)[0])

def hasANextIdentity(ident, char_set):
    try:
        next(filter(lambda x: x.ident == ident, char_set))
        return True
    except StopIteration:
        return False

def getNextValue(ident, char_set):
    try:
        ident = next(filter(lambda x: x.ident == ident, char_set))
        return ident.value
    except StopIteration:
        return None

def getType(myText, char_set):
    if myText.count('"') == 2:
        myText = myText.replace('\"', '')
        val = set([chr(ord(char)) for char in myText])
        return Node(NodeType['STRING'], val)
    if myText.count('\'') == 2:
        char = getText(myText)
        try:
            char = codecs.decode(char, 'unicode_escape')
            ord_ = ord(char)
        except:
            raise Exception(f'Unvalid char in GetElementType: {myText}')
        new_set = set(chr(ord_))
        return Node(NodeType['CHAR'], new_set)
    if myText in ['ANY']:
        if 'ANY' == myText:
            return Node(NodeType['STRING'], set([chr(char) for char in range(0, 256)]))
    if myText.isdigit():
        return Node(NodeType['NUMBER'], myText)
    if hasANextIdentity(myText, char_set):
        return Node(NodeType['ID'], getNextValue(myText, char_set), myText)
    if 'CHR' in myText:
        value = None
        start = myText.find('(')
        end = myText.find(')')
        if not (myText == -1 or end == -1) and not (myText.count('(') != 1 or myText.count(')') != 1):
            value = myText[start+1:end]
        if value == None:
            raise Exception(
                'Missed right parenthesis')
        if not value.isdigit():
            raise Exception(
                'Char is not defined correctly')
        char = set(chr(int(value)))
        return Node(NodeType['CHAR'], char)