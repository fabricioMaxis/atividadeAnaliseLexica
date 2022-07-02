class Token:
   def __init__(self, nome, lexema, linha=0, coluna=0, tipo=""):
      self.nome = nome
      self.lexema = lexema
      self.linha = linha
      self.coluna = coluna
      self.tipo = tipo

   def getNome(self):
      return self.nome

   def getLexema(self):
      return self.lexema

   def getLinha(self):
      return self.linha

   def setLinha(self, linha):
      self.linha = linha

   def getColuna(self):
      return self.coluna

   def setColuna(self, coluna):
      self.coluna = coluna

    

   def toString(self, linhaColuna = False):
        if linhaColuna:
            return "<" + str(self.nome.name) + ", \"" + str(self.lexema) + "\", " + str(self.linha) + ", " + str(self.coluna) + ">"
        else:
            return "<" + str(self.nome.name) + ", \"" + str(self.lexema) + "\">"

   def getTipo(self):
      return self.tipo
      
   def setTipo(self, tipo):
      self.tipo = tipo        