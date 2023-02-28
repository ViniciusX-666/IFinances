class Usuario:
    def __init__(self, nome, sobrenome, email, senha, id=None):
        self._id=id
        self._nome=nome
        self._sobrenome=sobrenome
        self._email=email
        self._senha=senha
        
    def getid(self):
        return self._id
    
class Despesas:
     def __init__(self,tipo,valor,data,id=None,idcliente= None):
        self._id = id
        self._tipo = tipo
        self._valor = valor
        self._data = data
        self._idcliente = idcliente
          
class Entrada:
    def __init__(self,tipo_entrada,valor_entrada,data_entrada,id=None,idcliente=None):
        self._id = id
        self._tipo_entrada = tipo_entrada
        self._valor_entrada = valor_entrada
        self._data_entrada = data_entrada
        self._idcliente = idcliente

class Poupanca:
    def __init__(self,tipo_poupanca,valor_poupanca,id=None, idcliente = None):
        self._id = id
        self._tipo_poupanca = tipo_poupanca
        self._valor_poupanca = valor_poupanca
        self._idcliente = idcliente

class ContasPagar:
     def __init__(self,conta,valor,data,id=None,idcliente= None):
        self._id = id
        self._conta = conta
        self._valor = valor
        self._data = data
        self._idcliente = idcliente

class ContasReceber:
     def __init__(self,tipo,valor,data,id=None,idcliente= None):
        self._id = id
        self._tipo = tipo
        self._valor = valor
        self._data = data
        self._idcliente = idcliente
