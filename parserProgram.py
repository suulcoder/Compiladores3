
### Disenio de Lenguajes de Programacion
### Saul Contreras
### Carnet 18409

import pickle

### Clase Parser creada a partir del arbol sintactico    
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        self.currentToken = None
        self.lastvalue = None

        self.nextToken = self.tokens[self.posicion]
        self.get()

        self.parser()

    def error(self, reporte):
        print(reporte)

    def expect(self, terminal):
        if self.currentToken == terminal:
            self.get()
        else:
            self.error('SINTAX ERROR')

    def get(self):
        if self.posicion - 1 < 0:
            self.lastvalue = None
        else:
            self.lastvalue = self.tokens[self.posicion - 1][1]

        if self.nextToken == None:
            self.currentToken = None
        else:
            self.currentToken = self.nextToken[0]
        self.posicion = self.posicion + 1

        if self.posicion >= len(self.tokens):
            self.nextToken = None
        else:
            self.nextToken = self.tokens[self.posicion]

    def parser(self):
        self.Expr()

    def Expr(self):
        while self.currentToken in ['token4', 'number', 'token7']:
        	if self.currentToken in ['token4', 'number', 'token7']:
        		self.Stat()
        		if self.currentToken == "token1":
        			self.expect("token1")
        if self.currentToken == "token2":
        	self.expect("token2")

    def Stat(self):
        value=0;
        value = self.Expression(value)
        print(value)

    def Expression(self, result):
        result1,result2 = 0,0;
        result1 = self.Term(result1)
        while self.currentToken in ['token3', 'token4']:
        	if self.currentToken == "token3":
        		self.expect("token3")
        		result2 = self.Term(result2)
        		result1+=result2
        	else:
        		if self.currentToken == "token4":
        			self.expect("token4")
        			result2 = self.Term(result2)
        			result1-=result2
        return result1

    def Term(self, result):
        result1,result2 = 0,0;
        result1 = self.Factor(result1)
        while self.currentToken in ['token5', 'token6']:
        	if self.currentToken == "token5":
        		self.expect("token5")
        		result2 = self.Factor(result2)
        		result1*=result2
        	else:
        		if self.currentToken == "token6":
        			self.expect("token6")
        			result2 = self.Factor(result2)
        			result1/=result2
        return result1

    def Factor(self, result):
        signo=1;
        if self.currentToken in ['token4']:
        	if self.currentToken == "token4":
        		self.expect("token4")
        		signo = -1;
        if self.currentToken in ['number']:
        	result = self.Number(result)
        else:
        	if self.currentToken == "token7":
        		self.expect("token7")
        		result = self.Expression(result)
        		if self.currentToken == "token8":
        			self.expect("token8")
        return result*signo

    def Number(self, result):
        if self.currentToken == "number":
        	self.expect("number")
        	return int(self.lastvalue)

### Lectura de pickle del Automata Serializado
with open('Pickle/tokensScanner.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Correr el Parser
parser = Parser(tokens)

parser.parser()