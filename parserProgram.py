
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
        elif(self.currentToken != None and terminal!=None and terminal!='white'):
            print('Sintax error: Expected value is ' + self.currentToken + ', Actual value is: ' + terminal)

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
        self.MyCOCOR()

    def MyCOCOR(self):
        CompilerName, EndName = "",""
        self.expect("token1")
        if self.currentToken in ['ident']:
        	CompilerName = self.Ident(CompilerName)
        	print("Nombre Inicial del Compilador ", CompilerName)
        	self.expect("Codigo")
        self.Body()
        self.expect("token2")
        if self.currentToken in ['ident']:
        	EndName = self.Ident(EndName)
        print("Nombre Final del Compilador: ",EndName)

    def Body(self):
        self.expect("Characters")
        self.expect("Keywords")
        self.expect("Tokens")
        self.expect("Productions")

    def Characters(self):
        while self.currentToken in []:
        	CharName, Counter = '',0
        	self.expect("token3")
        		print('LEYENDO CHARACTERS')
        	if self.currentToken in ['ident']:
        		CharName = self.Ident(CharName)
        		self.expect("token4")
        	else:
        	if self.currentToken in ['string', 'char', 'charnumber', 'charinterval', 'token21', 'ident']:
        		self.CharSet()
        		self.expect("token5")
        	self.CharSet()
        	self.expect("token6")
        	self.CharSet()
        	self.expect("token7")
        Counter+=1; print("Char Set ", Counter , " : ",CharName)

    def Keywords(self):
        KeyName,StringValue,Counter = '','',0
        self.expect("token8")
        while self.currentToken in []:
        		print('LEYENDO KEYWORDS')
        	if self.currentToken in ['ident']:
        		KeyName = self.Ident(KeyName)
        		Counter+=1;print("KeyWord ", Counter, " : ",KeyName)
        		self.expect("token4")
        		if self.currentToken in ['string']:
        			StringValue = self.String(StringValue)
        			if self.currentToken == "token7":
        				self.expect("token7")

    def Tokens(self):
        while self.currentToken in []:
        	TokenName, Counter = "", 0;
        	self.expect("token9")
        	print("LEYENDO TOKENS")
        	self.expect("Codigo")
        	if self.currentToken in ['ident']:
        		TokenName = self.Ident(TokenName)
        	Counter+=1;print("Token ", Counter,  " : ",TokenName)
        	self.expect("token4")
        	self.TokenExpr()
        	self.expect("ExceptKeyword")
        	self.expect("token7")

    def Productions(self):
        while self.currentToken in []:
        	Counter = 0
        	self.expect("token10")
        	ProdName = " "; print("LEYENDO PRODUCTIONS")
        	self.expect("Codigo")
        	if self.currentToken in ['ident']:
        		ProdName = self.Ident(ProdName)
        	Counter+=1; print("Production " ,Counter, " : " ,ProdName)
        	self.expect("Atributos")
        	self.expect("token4")
        	self.expect("Codigo")
        	if self.currentToken in ['string', 'char', 'ident', 'token13', 'token15', 'token17']:
        		self.ProductionExpr()
        	if self.currentToken == "token7":
        		self.expect("token7")

    def ExceptKeyword(self):
        self.expect("token11")
        self.expect("token8")

    def ProductionExpr(self):
        	self.ProdTerm()
        while self.currentToken in ['token12']:
        	if self.currentToken == "token12":
        		self.expect("token12")
        		self.ProdTerm()

    def ProdTerm(self):
        	self.ProdFactor()
        	self.expect("ProdFactor")

    def ProdFactor(self):
        else:
        else:
        else:
        if self.currentToken in ['string', 'char', 'ident']:
        	self.SymbolProd()
        self.expect("token13")
        self.ProductionExpr()
        self.expect("token14")
        self.expect("token15")
        self.ProductionExpr()
        self.expect("token16")
        self.expect("token17")
        self.ProductionExpr()
        self.expect("token18")
        self.expect("Codigo")

    def SymbolProd(self):
        else:
        	if self.currentToken in ['string']:
        		SV = self.String(SV)
        		print("String en Production: ",SV)
        	else:
        		if self.currentToken == "char":
        			self.expect("char")
        	if self.currentToken in ['ident']:
        		IN = self.Ident(IN)
        		print("Identificador en Production: ",IN)
        self.expect("Atributos")

    def Codigo(self):
        self.expect("startcode")
        self.expect("ANY")
        self.expect("endcode")

    def Atributos(self):
        self.expect("token19")
        self.expect("ANY")
        self.expect("token20")

    def TokenExpr(self):
        	self.TokenTerm()
        while self.currentToken in ['token12']:
        	if self.currentToken == "token12":
        		self.expect("token12")
        		self.TokenTerm()

    def TokenTerm(self):
        	self.TokenFactor()
        	self.expect("TokenFactor")

    def TokenFactor(self):
        else:
        else:
        if self.currentToken in ['string', 'char', 'ident']:
        	self.SimbolToken()
        self.expect("token13")
        self.TokenExpr()
        self.expect("token14")
        self.expect("token15")
        self.TokenExpr()
        self.expect("token16")

    def SimbolToken(self):
        IdentName, StringValue = "", ""
        if self.currentToken in ['string']:
        	StringValue = self.String(StringValue)
        else:
        	if self.currentToken == "char":
        		self.expect("char")
        else:
        if self.currentToken in ['ident']:
        	IdentName = self.Ident(IdentName)
        	print("Identificador en Token: ",IdentName)

    def CharSet(self):
        IdentName, StringValue = "",""
        if self.currentToken in ['string']:
        	StringValue = self.String(StringValue)
        else:
        	if self.currentToken in ['char', 'charnumber', 'charinterval']:
        		self.Char()
        else:
        if self.currentToken == "token21":
        	self.expect("token21")
        else:
        if self.currentToken in ['ident']:
        	IdentName = self.Ident(IdentName)
        print("Identificador en CharSet: ",IdentName)

    def Char(self):
        if self.currentToken == "char":
        	self.expect("char")
        elif self.currentToken == "charnumber":
        	self.expect("charnumber")
        else:
        if self.currentToken == "charinterval":
        	self.expect("charinterval")

    def String(self):
        if self.currentToken == "string":
        	self.expect("string")
        	return self.currentToken.value

    def Ident(self):
        if self.currentToken == "ident":
        	self.expect("ident")
        	return self.currentToken.value

### Lectura de pickle del Automata Serializado
with open('Pickle/tokensScanner.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Correr el Parser
parser = Parser(tokens)

parser.parser()