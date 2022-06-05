import sys

from ts import TS
from tag import Tag
from token import Token


class Lexer():
    

    def __init__(self, input_file):
        try:
            self.input_file = open(input_file, 'rb')
            self.lookahead = 0
            self.n_line = 1
            self.n_column = 0
            self.ts = TS()
            self.totalErros = 0
        except IOError:
            print('Erro de abertura do arquivo. Encerrando.')
            sys.exit(0)
    
    def closeFile(self):
        try:
            self.input_file.close()
        except IOError:
            print('Erro dao fechar arquivo. Encerrando.')
            sys.exit(0)

    def sinalizaErroLexico(self, message):
        self.totalErros = self.totalErros + 1
        print("[Erro Lexico]: ", message, "\n")

    def retornaPonteiro(self):
        if self.lookahead.decode('ascii') != '':
            self.input_file.seek(self.input_file.tell() - 1)
        self.n_column = self.n_column - 1

    def printTS(self):
        self.ts.printTS()

    def proxToken(self):
        ''' simula um AFD '''
        estado = 1
        lexema = ""
        c = '\u0000'

        while (True): 
            self.lookahead = self.input_file.read(1)
            c = self.lookahead.decode('ascii') # caractere lido
            self.n_column = self.n_column + 1

            if (estado == 1):
                if (c == ''):
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
                elif c == ' ' or c == '\t' or c == '\n' or c == '\r':
                    estado = 1
                    if c == '\n':
                        self.n_line = self.n_line + 1
                        self.n_column = 0
                    if c == '\t':
                        self.n_column = self.n_column + 3
                        
                elif (c == '+'):
                    return Token(Tag.OP_SOM, "+", self.n_line, self.n_column)
                elif (c == '-'):
                    
                    return Token(Tag.OP_SUB, "-", self.n_line, self.n_column)
                elif (c == '*'):
                    
                    return Token(Tag.OP_MULTI, "*", self.n_line, self.n_column)
                elif (c == '/'):
                    
                    return Token(Tag.OP_DIV, "/", self.n_line, self.n_column)
                elif (c == ':'):
                    
                    return Token(Tag.SMB_dois_pontos, ":", self.n_line, self.n_column)
                elif (c == ';'):
                    
                    return Token(Tag.SMB_ponto_virgula, ";", self.n_line, self.n_column)
                elif (c.isdigit()):
                    
                    lexema += c
                    estado = 2
                elif (c.isalpha()):
                    
                    lexema += c
                    estado = 3
                elif (c == '"'):
                    lexema += c
                    estado = 4
                elif c == '{':
                    estado = 5   
                else:
                    self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                                            str(self.n_line) + " e coluna " + str(self.n_column))
                    if self.totalErros == 5: 
                        print("Modo Pânico - Análise abortada")                      
                        return None
                    else:
                        estado = 1
                        lexema = ""
                        c = '\u0000'
                        continue    
            elif (estado == 2):
            
                if (c.isdigit()):
                    lexema += c
                else:
                    self.retornaPonteiro()
                    token = self.ts.getToken(lexema)
                    if (token is None):
                        token = Token(Tag.NUM, lexema, self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    else:
                        token.setColuna(self.n_column)
                        token.setLinha(self.n_line)
                        self.ts.updateLineColumn(lexema, self.n_line, self.n_column)

                    return token
                    
            elif (estado == 3):
                if (c.isalnum()):
                    lexema += c
                else:
                    self.retornaPonteiro()
                    token = self.ts.getToken(lexema)

                    if (token is None):
                        token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    else:
                        token.setColuna(self.n_column)
                        token.setLinha(self.n_line)
                        self.ts.updateLineColumn(lexema, self.n_line, self.n_column)

                    return token
            elif (estado == 4):
                if c == '"':
                    token = self.ts.getToken(lexema)
                    if (token is None):
                        token = Token(Tag.Literal, lexema, self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    else:
                        token.setColuna(self.n_column)
                        token.setLinha(self.n_line)
                        self.ts.updateLineColumn(lexema, self.n_line, self.n_column)

                    return token
                elif c == '\n':
                    self.sinalizaErroLexico("Caractere invalido [quebra de linha] na linha " + str(self.n_line) + " e coluna " + str(self.n_column))

                    if self.totalErros == 5:
                        print("Modo Pânico - Análise abortada")  
                        return None
                    else:
                        self.n_line = self.n_line + 1
                        estado = 1
                        lexema = ""
                        c = '\u0000'
                        continue
                elif c == '':
                    coluna = self.n_column
                    self.n_column = 0
                    return Token(Tag.Literal, lexema, self.n_line, coluna)
                elif c == '\t':
                    self.n_column = self.n_column + 3
                lexema += c

            elif estado == 5:
                if c=='}':
                        estado = 1
                elif c == '\n':
                    self.n_line = self.n_line + 1
                    self.n_column = 1
                    self.sinalizaErroLexico(
                  "Caractere invalido [quebra de linha] na linha " + str(self.n_line) + " e coluna " + str(
                     self.n_column))
                if self.totalErros == 5:
                  return None
                elif c == '':
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column - 1)
