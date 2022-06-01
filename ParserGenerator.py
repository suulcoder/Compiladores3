import pickle

class Token(object):
    def __init__(self, data):
        self.type = data[0]
        self.value = data[1]
        
def checkForConcat(tokens):
    for (index, token) in enumerate(tokens):
        if(
            index+1<len(tokens) and
            (
            token.token.type == 'ident' or
            token.token.type == 's_action' or
            token.token.type == 'string'
            ) 
        and 
            (
            tokens[index+1].token.type == 'ident' or
            tokens[index+1].token.type == 's_action' or
            tokens[index+1].token.type == 'string'
            )  
        ):
            return True
    return False
            
        
        
def consumeProduction(tokens):
    #Get code of idents and actions
    nodes = []
    _saved_tokens = []
    
    for (index, token) in enumerate(tokens):
        if(index in _saved_tokens):
            pass
        elif token.type == 's_action':
            nodes.append(Node(token, consumeCode(token)))
            _saved_tokens.append(index)
        elif token.type == 'string':
            nodes.append(Node(token, consumeString(token)))
            _saved_tokens.append(index)
        elif token.type=='ident':
            if(token.value == 'ANY'):
                local_code = '{tabs}self.currentToken=self.getToken()'.format(tabs = consumeWhileAndOr.counter*'\t')
                nodes.append(Node(token, local_code))
                _saved_tokens.append(index)
            #No Terminal
            elif(token.value[0].isupper()):
                if(tokens[index+1].type == 'attr'):
                    local_code = '{tabs}{attr} = self.{name}()'.format(name = token.value, attr=tokens[index+1].value[1:-1], tabs= consumeWhileAndOr.counter*'\t')
                    nodes.append(Node(token, local_code))
                    _saved_tokens.append(index)
                    _saved_tokens.append(index+1)
                else:
                    local_code = '{tabs}self.{name}()'.format(name=token.value, tabs=consumeWhileAndOr.counter*'\t')
                    nodes.append(Node(token, local_code))
                    _saved_tokens.append(index)
            #Terminales
            else:
                _code = '''
        {tabs}if(self.currentToken.type != '{type}'): 
        {tabs}    raise(self.currentToken.type, "was expected") 
        {tabs}    currentToken=self.getToken()'''.format(
            type = token.value,
            tabs = consumeWhileAndOr.counter*'\t'
            )
                local_code = """
        {_code}""".format(_code=_code)
                nodes.append(Node(token, local_code))
                _saved_tokens.append(index)
        else:
            nodes.append(Node(token))
                  
    #Remove []
    tokens = []
    sq_open_found = False
    p_open_found = False
    for node in nodes:
        if(node.token.type == 'sq_open'):
            sq_open_found = True
        elif(node.token.type == 'sq_close'):
            sq_open_found = False
        elif(node.token.type == 'p_open'):
            p_open_found = True
        elif(node.token.type == 'p_close'):
            p_open_found = False
        else:
            tokens.append(node)
    if(sq_open_found):
        print("[ was not closed")  
    if(p_open_found):
        print("[ was not closed")  
      
    nodes = []
    saved_tokens = []
    for (index, token) in enumerate(tokens):
        if(index in saved_tokens):
            continue
        elif(
            token.token.type == 'ident' or
            token.token.type == 's_action' or
            token.token.type == 'string'
        ):
            local_index = 1
            saved_tokens.append(index)
            code = token.code + ';'
            while (
                index+local_index<len(tokens) and 
                (tokens[index+local_index].token.type == 'ident' or
                tokens[index+local_index].token.type == 's_action' or
                tokens[index+local_index].token.type == 'string')
                ):
                saved_tokens.append(index+local_index)
                code += tokens[index+local_index].code + ';'
                local_index += 1
            nodes.append(Node(token.token, code))
        else:
            nodes.append(token)    
    
    
    
    tokens = []
    saved_tokens = []
    for (index, node) in enumerate(nodes):
        if(
            node.token.type == 'br_open' and 
            nodes[index+1].token.value == 'ANY' and 
            nodes[index+2].token.type == 'br_close'):
            tokens.append(
                Node(
                    Token(('procesed', 'ANY')), 
                    code='''
        {tabs}while(True):
        {tabs}    {code}
        {tabs}    if(self.currentToken.value=='{value}'): 
        {tabs}        break'''.format(
                        tabs = consumeWhileAndOr.counter*'\t',
                        code = nodes[index+1].code,
                        value = nodes[index+3].token.value
                        )
                    )
                )
            saved_tokens.append(index)
            saved_tokens.append(index+1)
            saved_tokens.append(index+2)
            saved_tokens.append(index+3)
        elif(index not in saved_tokens):
            tokens.append(node)
            
    
            
    return consumeWhileAndOr(tokens)

def consumeWhileAndOr(tokens):
    nodes = []
    while_tokens = []
    onWhile = False
    orFound = False
    returnCode = True
    for (index, node) in enumerate(tokens):
        if(node.token.type == 'br_open'):
            onWhile = True
            returnCode = False
        elif(node.token.type == 'br_close'):
            code = """
        {tabs}#Start of br_open
        {tabs}entry_index_{loop_number} = self.index
        {tabs}while(True):
        {tabs}    entry_index_{loop_number} = self.index
        {tabs}    try:
        {tabs}        {code}
        {tabs}    except:
        {tabs}        self.index = entry_index_{loop_number}
        {tabs}        break
        {tabs}#End of br_close""".format(
                code=consumeWhileAndOr(while_tokens),
                loop_number=consumeWhileAndOr.counter,
                tabs=consumeWhileAndOr.counter*'\t',
            )
            nodes.append(Node(node.token, code))
            onWhile = False
            while_tokens = []
            consumeWhileAndOr.counter += 1
        elif(onWhile):
            while_tokens.append(node)
        elif(
            index+1<len(tokens) and 
            tokens[index+1].token.type == 'union'):
            code = '''
        {tabs}#When Union is found we must do a try except
        {tabs}entry_index_{loop_number} = self.index
        {tabs}try:
        {tabs}  {code1}
        {tabs}except:
        {tabs}   self.index = entry_index_{loop_number}
        {tabs}  {code2}
        {tabs}#End of Or'''.format(
                loop_number=consumeWhileAndOr.counter,
                tabs=consumeWhileAndOr.counter*'\t',
                code1=node.code,
                code2=consumeWhileAndOr(nodes[index+1:]),   
            )
            nodes.append(Node(node.token, code))
            orFound = True
            returnCode = False
            consumeWhileAndOr.counter += 1
        elif(not orFound):
            nodes.append(node)
    if(returnCode and len(nodes)==1):
        return nodes[0].code
    else:
        returnCode = ''
        for node in nodes:
            returnCode += node.code
        return returnCode

def consumeCode(token):
    #Remove (. and .)
    return token.value[2:-2]

def consumeString(token):
    #Tell parser to expect the value of the string
    return ('{tabs}self.expect(\'{}\')'.format(token.value[1:-1], tabs=consumeWhileAndOr.counter*'\t'))
        
class Node(object):
    def __init__(self, token, code=None):
        self.token = token
        self.code=code
    
        
class ParserGenerator(object):
    def __init__(self):
        self.code = """

#Saul Contreras
#Parser
#Universidad del Valle

import pickle

class Token(object):
    def __init__(self, data):
        self.type = data[0]
        self.value = data[1]

class Parser(object):
    def __init__(self):
        self.tokens = [] 
        ### Read pickle Tokens
        with open('Pickle/tokensScanner.pickle', 'rb') as f:
            self.tokens = pickle.load(f)
            
        self.index = 0
        self.currentToken = self.getToken()

    def getToken(self):
        try:
            token = Token(self.tokens[index])
            index += 1
            return token
        except:
            print("End of tokens")
            return None
    


    def expect(self,expected):
        if(self.currentToken.value==expected):
            self.currentToken=self.getToken()
            return True
        raise(expected, " was expected bug a ", self.currentToken.type, " was provided. ")
"""
        
        self.grammarTokens = []

        #Lets get the tokens from the grammar:
        with open('Pickle/productions.pickle', 'rb') as f:
            self.grammarTokens = pickle.load(f)
            
        self.index = 0
        self.currentToken = self.getToken()
        
        while self.currentToken!=None:
            # When a production is declared:
            # It is an ident with the Name of the Produciton followed by an eq:
            if(self.currentToken.type=='ident' and self.peekToken(0)!=None and self.peekToken(0).type=='eq'):
                #First lets do some validations:
                
                has_end = False
                
                #We are expecting a '.' or p_end
                temporal_index = 1
                local_production_tokens = []
                next_token = self.peekToken(temporal_index)
                while next_token!=None and not has_end: 
                    if next_token.type=='p_end':
                        has_end=True
                    else:
                        local_production_tokens.append(next_token)
                    temporal_index+=1
                    next_token = self.peekToken(temporal_index)
                
                if(not has_end):
                    raise("Declared production ", self.currentToken.value, " has not p_end")
                
                if(not self.currentToken.value[0].isupper()):
                    raise("Production name must be uppercase ", self.currentToken.value)
                
                consumeWhileAndOr.counter = 0
                production_code = consumeProduction(local_production_tokens)
                
                print("")
                print("")
                    
                self.code += """
    #Production {productionName}
    def {productionName}(self):
        {production_code}
        """.format(
            productionName = self.currentToken.value,
            production_code = production_code
            )
            self.currentToken = self.getToken()
        text_file = open("parser.py", "w")
        text_file.write(self.code)
        text_file.close()


    def getToken(self):
        try:
            token = Token(self.grammarTokens[self.index])
            self.index += 1
            return token
        except:
            return None
        
    def peekToken(self,i):
        try:
            return Token(self.grammarTokens[self.index+i])
        except:
            return None

ParserGenerator()