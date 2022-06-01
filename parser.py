

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
        self.MyCOCOR()

    def getToken(self):
        try:
            token = Token(self.tokens[self.index])
            self.index += 1
            if(token.type == 'nontoken'):
                return self.getToken()
            return token
        except:
            return None
    


    def expect(self,expected):
        if(self.currentToken.value==expected):
            self.currentToken=self.getToken()
            return True
        raise BaseException(expected, " was expected but a ", self.currentToken.type, " was provided. with value", self.currentToken.value)

    #Production MyCOCOR
    def MyCOCOR(self):
        CompilerName, EndName = "","";self.expect('COMPILER');CompilerName = self.Ident();print("Nombre Inicial del Compilador ", CompilerName);self.Codigo();self.Body();self.expect('END');EndName = self.Ident();print("Nombre Final del Compilador: ",EndName);
        
    #Production Body
    def Body(self):
        self.Characters();self.Keywords();self.Tokens();self.Productions();
        
    #Production Characters
    def Characters(self):
        CharName, Counter = "",0;self.expect('CHARACTERS');print("LEYENDO CHARACTERS");self.Codigo();
        	#Start of br_open
        entry_index_0 = self.index
        while(self.currentToken.value!='KEYWORDS'):
            entry_index_0 = self.index
            CharName = self.Ident();Counter+=1; print("Char Set ", Counter , " : ",CharName);self.expect('=');
            while(True):
                if(self.currentToken.type == 'ident'):
                    print("Identificador en Char Set: ",self.currentToken.value)
                if(self.currentToken.value=='.'): 
                    self.currentToken=self.getToken();
                    break
                self.currentToken=self.getToken();
            # try:
                
            #     entry_index_1 = self.index
            #     CharName = self.Ident();Counter+=1; print("Char Set ", Counter , " : ",CharName);self.expect('=');self.CharSet();
            #     try:
            #         #When Union is found we must do a try except
            #         entry_index_2 = self.index
            #         try:
            #             self.expect('+');self.CharSet();
            #         except BaseException as e:
            #             self.expect('-');self.CharSet();
            #             self.index = entry_index_2 - 1
            #     except BaseException as e:
            #         pass
            #         #self.index = entry_index_1 - 1
        	        
          
            #      #End of Or
            #     entry_index_0 = self.index
            #     self.expect('.')
            # except BaseException as e:
            #     self.index = entry_index_0 - 1
            #     self.currentToken = self.getToken()
            #     return
            #     break
        	#End of br_close
        
    #Production Keywords
    def Keywords(self):
        KeyName,StringValue,Counter = "","",0;self.expect('KEYWORDS');print("LEYENDO KEYWORDS");self.Codigo();
        #Start of br_open
        entry_index_0 = self.index
        while(self.currentToken.value!='TOKENS'):
            try:
                KeyName = self.Ident();Counter+=1;print("KeyWord ", Counter, " : ",KeyName);self.expect('=');StringValue = self.String();self.expect('.');
            except BaseException as e:
                self.index = entry_index_0 + 7
                self.currentToken = self.getToken()
                return
            entry_index_0 = self.index
        #End of br_close
        
    #Production Tokens
    def Tokens(self):
        TokenName, Counter = "", 0;self.expect('TOKENS');print("LEYENDO TOKENS");self.Codigo();
        #Start of br_open
        entry_index_0 = self.index
        while(self.currentToken.value!='PRODUCTIONS'):
            try:
                TokenName = self.Ident();Counter+=1;print("Token ", Counter,  " : ",TokenName);self.expect('=');
                #self.TokenExpr();
                #self.ExceptKeyword();self.expect('.');
                while(True):
                    if(self.currentToken.type == 'ident'):
                        print("Identificador en Token: ",self.currentToken.value)
                    if(self.currentToken.value=='.'): 
                        self.currentToken=self.getToken();
                        break
                    self.currentToken=self.getToken();
            except BaseException as e:
                pass    
                entry_index_0 = self.index
        #End of br_close
        
    #Production Productions
    def Productions(self):
        Counter = 0;self.expect('PRODUCTIONS');ProdName = " "; print("LEYENDO PRODUCTIONS");self.Codigo();
        #Start of br_open
        entry_index_0 = self.index
        ignore = False
        while(self.currentToken.value!='END'):
            entry_index_0 = self.index
            ProdName = self.Ident();Counter+=1; print("Production " ,Counter, " : " ,ProdName);
            #self.Atributos();self.expect('=');self.Codigo();self.ProductionExpr();self.expect('.');
            while(True):
                if(self.currentToken.value == '(.' or self.currentToken.value == '<'):
                    ignore = True
                if(self.currentToken.value == '.)' or self.currentToken.value == '>'):
                    ignore = False
                if(self.currentToken.type == 'ident' and not ignore):
                    print("Identificador en Production: ",self.currentToken.value)
                if(self.currentToken.type == 'string' and not ignore):
                    print("String en Production: ",self.currentToken.value)
                if(self.currentToken.value=='.' and not ignore):
                    self.currentToken=self.getToken();
                    break
                self.currentToken=self.getToken();
        #End of br_close
        
    #Production ExceptKeyword
    def ExceptKeyword(self):
        self.expect('EXCEPT');self.expect('KEYWORDS');
        
    #Production ProductionExpr
    def ProductionExpr(self):
        self.ProdTerm();
        #Start of br_open
        entry_index_0 = self.index
        while(True):
            entry_index_0 = self.index
            try:
                self.expect('|');self.ProdTerm();
            except:
                self.index = entry_index_0
                break
        #End of br_close
        
    #Production ProdTerm
    def ProdTerm(self):
        self.ProdFactor();
        #Start of br_open
        entry_index_0 = self.index
        while(True):
            entry_index_0 = self.index
            try:
                self.ProdFactor();
            except:
                self.index = entry_index_0
                break
        #End of br_close
        
    #Production ProdFactor
    def ProdFactor(self):
        
        #When Union is found we must do a try except
        entry_index_0 = self.index
        try:
          self.SymbolProd();
        except:
            self.index = entry_index_0
          
        #End of Or
        	#When Union is found we must do a try except
            entry_index_1 = self.index
            try:
                self.expect('(');self.ProductionExpr();self.expect(')');
            except:
                self.index = entry_index_1
        	  
        	#End of Or
        		#When Union is found we must do a try except
                entry_index_2 = self.index
                try:
                    self.expect('[');self.ProductionExpr();self.expect(']');
                except:
                    self.index = entry_index_2
        		  
        		#End of Or
        
    #Production SymbolProd
    def SymbolProd(self):
        
        #When Union is found we must do a try except
        entry_index_0 = self.index
        try:
          SV, IN = "","";SV = self.String();print("String en Production: ",SV);
        except:
            self.index = entry_index_0
          
        #End of Or
        	#When Union is found we must do a try except
            entry_index_1 = self.index
            try:
        	  
                if(self.currentToken.type != 'char'): 
                    raise BaseException(self.currentToken.type, "was expected") 
                currentToken=self.getToken();
            except:
                self.index = entry_index_1
        	  
        	#End of Or
        
    #Production Codigo
    def Codigo(self):
        
        
        if(self.currentToken.type != 'startcode'): 
            print(self.currentToken.type, "was expected") 
        self.currentToken=self.getToken();
        while(True):
            self.currentToken=self.getToken();
            if(self.currentToken.type=='endcode'): 
                self.currentToken=self.getToken();
                break
        
    #Production Atributos
    def Atributos(self):
        self.expect('<');
        while(True):
            self.currentToken=self.getToken();
            if(self.currentToken.value=='">"'): 
                break
        
    #Production TokenExpr
    def TokenExpr(self):
        self.TokenTerm();
        #Start of br_open
        entry_index_0 = self.index
        while(True):
            entry_index_0 = self.index
            try:
                self.expect('|');self.TokenTerm();
            except:
                self.index = entry_index_0
                break
        #End of br_close
        
    #Production TokenTerm
    def TokenTerm(self):
        self.TokenFactor();
        #Start of br_open
        entry_index_0 = self.index
        while(True):
            entry_index_0 = self.index
            try:
                self.TokenFactor();
            except:
                self.index = entry_index_0
                break
        #End of br_close
        
    #Production TokenFactor
    def TokenFactor(self):
        
        #When Union is found we must do a try except
        entry_index_0 = self.index
        try:
          self.SimbolToken();
        except:
            self.index = entry_index_0
          
        #End of Or
        	#When Union is found we must do a try except
            entry_index_1 = self.index
            try:
                self.expect('(');self.TokenExpr();self.expect(')');
            except:
                self.index = entry_index_1
        	  
        	#End of Or
        
    #Production SimbolToken
    def SimbolToken(self):
        
        #When Union is found we must do a try except
        entry_index_0 = self.index
        try:
          IdentName, StringValue = "", "";StringValue = self.String();
        except:
            self.index = entry_index_0
          
        #End of Or
        	#When Union is found we must do a try except
            entry_index_1 = self.index
            try:
        	  
        
                if(self.currentToken.type != 'char'): 
                    raise BaseException(self.currentToken.type, "was expected") 
                self.currentToken=self.getToken();
            except:
                self.index = entry_index_1
        	  
        	#End of Or
        
    #Production CharSet
    def CharSet(self):
        
        #When Union is found we must do a try except
        entry_index_0 = self.index
        try:
          IdentName, StringValue = "","";StringValue = self.String();
        except:
            self.index = entry_index_0
          
        #End of Or
        	#When Union is found we must do a try except
            entry_index_1 = self.index
            try:
                self.Char();
            except:
                self.index = entry_index_1
        	  
        	#End of Or
        		#When Union is found we must do a try except
                entry_index_2 = self.index
                try:
                    self.expect('ANY');
                except:
                    self.index = entry_index_2
        		  
        		#End of Or
        
    #Production Char
    def Char(self):
        
        #When Union is found we must do a try except
        entry_index_0 = self.index
        try:
          
        
            if(self.currentToken.type != 'char'): 
                raise BaseException(self.currentToken.type, "was expected") 
            self.currentToken=self.getToken();
        except:
            self.index = entry_index_0
          
        #End of Or
        	#When Union is found we must do a try except
            entry_index_1 = self.index
            try:
        	  
        
                if(self.currentToken.type != 'charnumber'): 
                    raise BaseException(self.currentToken.type, "was expected") 
                self.currentToken=self.getToken();
            except:
                self.index = entry_index_1
        	  
        	#End of Or
        
    #Production String
    def String(self):
        
        if(self.currentToken.type != 'string'): 
            raise BaseException(self.currentToken.type, "was expected") 
        toReturn = self.currentToken.value;
        self.currentToken=self.getToken();return toReturn;
        
    #Production Identz
    def Ident(self):
        if(self.currentToken.type != 'ident'): 
            raise BaseException("ident was expected but ", self.currentToken.type, " found") 
        toReturn = self.currentToken.value;
        self.currentToken=self.getToken();return toReturn;
        
Parser()