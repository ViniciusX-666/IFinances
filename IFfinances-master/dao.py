from models import ContasPagar, Usuario, Despesas, ContasPagar,Entrada, Poupanca, ContasReceber

SQL_CRIA_CLIENTE = 'INSERT into cliente (nome,sobrenome,email,senha) values (%s, %s, %s, %s)'
SQL_DELETA_CLIENTE = 'DELETE from cliente where idcliente=%s'
SQL_ATUALIZA_CLIENTE = 'UPDATE cliente SET nome=%s,sobrenome=%s,email=%s, senha=%s where idcliente=%s'
SQL_USUARIO_POR_ID = 'SELECT idcliente,nome,sobrenome,email,senha from cliente where email=%s '
SQL_BUSCA_CLIENTE = 'SELECT id,nome,sobrenome,usuario,email,senha from cliente where id=%s '
SQL_BUSCA_CONTA ='SELECT nome,sobrenome from cliente where idcliente=%s'
SQL_BUSCA_NOME = 'SELECT nome from cliente where idcliente=%s'
SQL_BUSCA_SOBRENOME = 'SELECT sobrenome from cliente where idcliente=%s'
SQL_BUSCA_EMAIL = 'SELECT email from cliente where idcliente=%s'
SQL_SOMA_TOTAL = 'SELECT valor FROM `total3` WHERE cod=%s'
#-----------------------------------------------------------------------------------------------------
SQL_ATUALIZA_DESPESAS = ''
SQL_CRIA_DESPESAS = 'INSERT into despesas (valor, dta_vencimento,tipodesp_idtipo,idcliente) values (%s,%s, %s,%s)'
SQL_DELETA_DESPESAS = 'DELETE from despesas where iddespesas=%s'
SQL_ATUALIZA_DESPESAS = 'UPDATE despesas SET  tipodesp_idtipo = %s, valor = %s, dta_vencimento = %s, idcliente = %s where iddespesas=%s '
SQL_BUSCA_DESPESAS = 'SELECT  iddespesas, tipodesp_idtipo, valor, dta_vencimento  from despesas WHERE idcliente = %s'
SQL_DESPESAS_POR_ID = 'SELECT  iddespesas, valor, dta_vencimento,tipodesp_idtipo from despesas where iddespesas=%s'
SQL_SOMA_DESPESA = 'SELECT SUM(valor) from despesas WHERE idcliente = %s'
#-----------------------------------------------------------------------------------------------------------
SQL_ATUALIZA_ENTRADAS = 'UPDATE entradas SET valor_entrada = %s, dta_entrada = %s,tipoentrada_idtipo = %s  where identradas=%s '
SQL_CRIA_ENTRADAS = 'INSERT into entradas (valor_entrada, dta_entrada,tipoentrada_idtipo,idcliente) values (%s,%s, %s, %s)'
SQL_SOMA_ENTRADA = 'SELECT SUM(valor_entrada) from entradas WHERE idcliente = %s'
#--------------------------------------------------------------------------------------------------------------
SQL_ATUALIZA_POUPANCA = 'UPDATE entradas SET valor_poupanca = %s,tipopoupanca_idtipo = %s, idcliente = %s  where idpoupanca=%s '
SQL_CRIA_POUPANCA = 'INSERT into poupancas (valor_poupanca, tipopoupanca_idtipo,idcliente) values (%s,%s,%s)'
SQL_SOMA_POUPANCA = 'SELECT SUM(valor_poupanca) FROM poupancas WHERE idcliente = %s'
#-------------------------------------------------------------------------------------------------------------
SQL_CRIA_CONTA_PAGAR = 'INSERT into pagar (tipo,valor,datapagar,idcliente) values (%s, %s,%s,%s)'
SQL_BUSCA_PAGAR = 'SELECT  idpagar,datapagar, tipo, valor from pagar WHERE idcliente = %s'
#--------------------------------------------------------------------------------------------------------------
SQL_CRIA_CONTA_RECEBER = 'INSERT into receber (tipo,valor,datareceber,idcliente) values (%s, %s,%s,%s)'
SQL_BUSCA_RECEBER = 'SELECT  idreceber, datareceber, tipo,valor  from receber WHERE idcliente = %s'

def traduz_usuario(tupla):    
   # return Usuario(tupla[1],tupla[2],tupla[3],tupla[4],tupla[5],tupla[0])
   return Usuario(tupla[1],tupla[2],tupla[3],tupla[4], tupla[0])
    
class UsuarioDao:
    def busca_por_id(self,email):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID,(email,))
        dados = cursor.fetchone()
        cliente = traduz_usuario(dados) if dados else None
        return cliente
          

    def __init__(self,db):
        self.__db=db
        #cria e atualiza usuario
    def salvar(self,cliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_CLIENTE,(cliente._nome,cliente._sobrenome,cliente._email,cliente._senha))
        self.__db.connection.commit()
        
        return cliente

    def atualizarConta(self,cliente,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ATUALIZA_CLIENTE,(cliente,idcliente,))
        self.__db.connection.commit()

    #Deleta usuario
    def deletar_usuario(self,id):
        self.__db.connection.cursor().execute(SQL_DELETA_CLIENTE,(id,))
        self.__db.connection.commit()
    
    def conta(self,id):
         self.__db.connection.cursor().execute(SQL_BUSCA_CONTA,(id,))

    def listar_nome(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_NOME,(idcliente,))
        nome = cursor.fetchone()
        self.__db.connection.commit()   
        return nome

    def listar_sobrenome(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_SOBRENOME,(idcliente,))
        sobrenome = cursor.fetchone()
        self.__db.connection.commit()   
        return sobrenome

    def listar_email(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_EMAIL,(idcliente,))
        email = cursor.fetchone()
        self.__db.connection.commit()   
        return email
        


class DespesasDao:  
    def __init__(self,db):
        self.__db=db         
        
    def salvar(self,despesas):
        cursor = self.__db.connection.cursor()

        if(despesas._id):
           
            cursor.execute(SQL_ATUALIZA_DESPESAS,(despesas._valor,despesas._data,despesas._tipo,despesas._idcliente, despesas._id,))
        else:
            cursor.execute(SQL_CRIA_DESPESAS,(despesas._valor,despesas._data,despesas._tipo,despesas._idcliente))
           
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        
        return despesas
    
    def listar(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_DESPESAS,(idcliente,))
        despesas = traduz_despesas(cursor.fetchall())
        self.__db.connection.commit()   
        return despesas
    #--------------------------------------------------
    def busca_por_id(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_DESPESAS_POR_ID,(idcliente,))
        tupla = cursor.fetchone()
        print(tupla)
        return Despesas(tupla[1], tupla[2], tupla[3] , id= tupla[0])
    #--------------------------------------------------
    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_DESPESAS,(id,))
        self.__db.connection.commit() 

    def somar(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SOMA_DESPESA,(idcliente,)) 
        somas = cursor.fetchone()
        return somas 

    def somar_total(self,cod):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SOMA_TOTAL,(cod,)) 
        soma_total = cursor.fetchone()
        return soma_total


def traduz_despesas(despesas):
    def cria_despesas_com_tupla(tupla):
        print(tupla)
        return(Despesas(tupla[3],tupla[1],tupla[2],tupla[0]))
    return list(map(cria_despesas_com_tupla,despesas))    


class EntradaDao:
    def __init__(self,db):
        self.__db=db

    def salvar(self,entrada):
        cursor = self.__db.connection.cursor()

        if(entrada._id):
           
            cursor.execute(SQL_ATUALIZA_ENTRADAS,(entrada._valor_entrada,entrada._data_entrada,entrada._tipo_entrada, entrada._id,entrada._idcliente))
        else:
            cursor.execute(SQL_CRIA_ENTRADAS,(entrada._valor_entrada,entrada._data_entrada,entrada._tipo_entrada,entrada._idcliente))
           
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        
        return entrada

    def somar(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SOMA_ENTRADA,(idcliente,)) 
        self.__db.connection.commit() #commit
        somas = cursor.fetchone()
        return somas 

class PoupancaDao:
    def __init__(self,db):
        self.__db=db

    def salvar(self,poupanca):
        cursor = self.__db.connection.cursor()

        if(poupanca._id):
           
            cursor.execute(SQL_ATUALIZA_POUPANCA,(poupanca._valor_poupanca,poupanca._tipo_poupanca, poupanca._id, poupanca._id))
        else:
            cursor.execute(SQL_CRIA_POUPANCA,(poupanca._valor_poupanca,poupanca._tipo_poupanca,poupanca._idcliente))
           
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        
        return poupanca

    def somar(self,idcliente):
         cursor = self.__db.connection.cursor()
         cursor.execute(SQL_SOMA_POUPANCA,(idcliente,)) 
         somas = cursor.fetchone()
         return somas
    def somar_total(self,cod):
         cursor = self.__db.connection.cursor()
         cursor.execute(SQL_SOMA_POUPANCA,(cod,)) 
         somastotal = cursor.fetchone()
         return somastotal

class ContasPagarDao:  
    def __init__(self,db):
        self.__db=db         
        
    def salvar(self,contas):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_CONTA_PAGAR,(contas._conta,contas._valor,contas._data,contas._idcliente))
        cursor._id = cursor.lastrowid
        self.__db.connection.commit()
        
        return contas
    def listar(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_PAGAR,(idcliente,))
        pagamento = traduz_contas(cursor.fetchall())
        self.__db.connection.commit()   
        return pagamento

def traduz_contas(pagamento):
    def cria_contas_com_tupla(tupla):
        print(tupla)
        return(ContasPagar(tupla[2],tupla[3],tupla[1]))
    return list(map(cria_contas_com_tupla,pagamento))

class ContasReceberDao:  
    def __init__(self,db):
        self.__db=db         
        
    def salvar(self,receber):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_CONTA_RECEBER,(receber._tipo,receber._valor,receber._data,receber._idcliente))
        cursor._id = cursor.lastrowid
        self.__db.connection.commit()
    
    def listar(self,idcliente):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_RECEBER,(idcliente,))
        recebimento = traduz_recebimentos(cursor.fetchall())
        self.__db.connection.commit()   
        return recebimento

def traduz_recebimentos(recebimento):
    def cria_recebimento_com_tupla(tupla):
        return ContasReceber(tupla[3],tupla[1],tupla[2])
    return list(map(cria_recebimento_com_tupla,recebimento))


    

