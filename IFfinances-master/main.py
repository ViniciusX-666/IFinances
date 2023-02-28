from flask import Flask, render_template, request, redirect, flash, session, send_from_directory

from dao import UsuarioDao, DespesasDao, EntradaDao, PoupancaDao, ContasPagarDao, ContasReceberDao
from flask_mysqldb import  MySQL

import os 

from models import Usuario, Despesas, Entrada, Poupanca, ContasPagar, ContasReceber

app = Flask(__name__)
app.secret_key = 'engenharia'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mf'
app.config['MYSQL_PORT'] = 3306
db = MySQL(app)

#convertando o banco de dados
usuario_dao = UsuarioDao(db)
despesas_dao = DespesasDao(db)
entrada_dao = EntradaDao(db)
poupanca_dao = PoupancaDao(db)
contas_dao = ContasPagarDao(db)
receber_dao = ContasReceberDao(db)

#login 
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima=''
    return render_template('login.html',proxima=proxima)


#------------------------------------------------------------------------------
@app.route('/autenticar', methods=['POST',])
def autenticar():    
    usuario=usuario_dao.busca_por_id(request.form['usuario'])
    global idcliente
    idcliente = usuario.getid()
    print(idcliente)
    if usuario: 
        print('loguei')
        if usuario._senha == request.form['senha']:
            session['usuario_logado']=request.form['usuario']
            flash(request.form['usuario'] + ' logado com sucesso!','sucesso')
            proxima_pagina = request.form['proxima']
            if proxima_pagina == 'None':
                return redirect('/')
            else:
                return redirect('/')  
    print('nao loguei')       
    flash('Não logado','sucesso')
    return redirect('/login')

@app.route('/')
@app.route('/index')
def index():
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        print('usuario_logado')
        return redirect('/login?proxima=index')
    
    lista = despesas_dao.listar(idcliente)
    listas = contas_dao.listar(idcliente)
    soma = poupanca_dao.somar(idcliente)[0]
    despesa_somar = despesas_dao.somar(idcliente)[0]
    # somar_total = despesas_dao.somar_total(cod=idcliente)[0]
    
    entrada_somar = entrada_dao.somar(idcliente)[0]
    

    
    return render_template('Dashboard.html',despesas = lista, poupar = soma, pagamento = listas, despesa = despesa_somar, entrada = entrada_somar)

#REGISTRO DE USUÁRIO
@app.route('/cadastro')
def cadastro():
    proxima2= request.args.get('proxima2')
    return render_template('cadastro.html',proxima2=proxima2)

@app.route('/salvarUsuario', methods=['POST',])
def salvarUsuario():
    
    nome = request.form['name']
    sobrenome = request.form['lastname']
    email = request.form['email']
    senha = request.form['password']  

    cadastro = Usuario(nome,sobrenome,email,senha)
    
    usuario_dao.salvar(cadastro)
    return redirect('/login')

@app.route('/deletar_cliente/<int:id>')
def deletar_cliente(idcliente):
    usuario_dao.deletar_usuario(idcliente)
    return redirect('/login')


#-------------------------------------------------------------------
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    
    flash( ' Nenhum usuario logado','sucesso')
    return redirect('/login')


# Rota para inserir imagens nos html
@app.route('/img/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('img', nome_arquivo)

@app.route('/saldo')
def saldo():
    return render_template('Saldo.html',titulo = "Insira seu saldo")


@app.route('/despesas')
def despesas():
    #código pra verificar se estar logado
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=index')
   
    return render_template('despesas.html', titulo = "Gerencie suas despesas")

@app.route('/salvarDespesas', methods=['POST',])
def salvarDespesas():
        
    tipo = request.form['tipo']
    valor = request.form['valor']
    data = request.form['data']
    
    despesas = Despesas(tipo,valor,data,idcliente=idcliente)
    despesas_dao.salvar(despesas)
    flash(' Despesa salva com sucesso!','sucesso')
    return redirect('/despesas')

#deletar
@app.route('/deletar/<int:id>')
def deletar(id):
    despesas_dao.deletar(id)
    return redirect('/')
#--------------------------------------------------
#update
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=editar')
    lista = despesas_dao.busca_por_id(id)    
    return render_template('editarDespesas.html', titulo = 'Editar despesas',despesas = lista)  
    
@app.route('/editarDespesas', methods=['POST',])
def editarDespesas():
    
    tipo = request.form['tipo']
    valor = request.form['valor']
    data = request.form['data']
    id = request.form['id']
    despesas = Despesas(tipo,valor,data,id)
    
    despesas_dao.salvar(despesas)
    flash(' Despesa atualizada com sucesso!','sucesso')
    return redirect('/')      

#-----------------Entradas--------------------------------
#entradas
@app.route('/entradas')
def entrada():
    #código pra verificar se estar logado
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=index')
   
    return render_template('entradas.html', titulo = "Gerencie suas Entradas")

@app.route('/salvarEntrada', methods=['POST',])
def salvarEntrada():
    
    tipo_entrada = request.form['tipo_entrada']
    valor_entrada = request.form['valor_entrada']
    data_entrada = request.form['data_entrada']
    
    entrada = Entrada(tipo_entrada,valor_entrada,data_entrada,idcliente=idcliente)
    
    entrada_dao.salvar(entrada)
    flash(' Entrada salva com sucesso!','sucesso')
    return redirect('/')  

@app.route('/poupanca')
def poupanca():
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=index')
   
    return render_template('poupanca.html', titulo = "Gerencie suas poupanca")

@app.route('/salvarPoupanca', methods=['POST',])
def salvarPoupanca():
    
    tipo_poupanca = request.form['tipo_poupanca']
    valor_poupanca = request.form['valor_poupanca']
    
    
    poupanca = Poupanca(tipo_poupanca,valor_poupanca,idcliente=idcliente)
    
    poupanca_dao.salvar(poupanca)
    flash('Parabéns, Você incluiu uma poupança!','sucesso')
    return redirect('/') 

#------------------CONTA---------------------------
@app.route('/conta')
def conta():
    
    nome_usuario=usuario_dao.listar_nome(idcliente)[0]
    sobrenome_usuario=usuario_dao.listar_sobrenome(idcliente)[0]
    email_usuario=usuario_dao.listar_email(idcliente)[0]
       
    return render_template('conta.html', titulo = "Minha Conta", nome = nome_usuario, sobrenome = sobrenome_usuario, email = email_usuario)

@app.route('/atualizar_conta', methods=['POST',])
def atualizarConta():  
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    email = request.form['email']
    senha = request.form['senha']
    
    
    cliente = Usuario(nome,sobrenome,email,senha)
    print(nome)
    print(email)
    print(sobrenome)
    print(idcliente)
    
    
    usuario_dao.atualizarConta(cliente,idcliente)
    return redirect('/despesas')

@app.route('/contas_pagar')
def contas_pagar():
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=index')
   
    return render_template('contas_pagar.html', titulo = "Cadastre suas Contas a Pagar")

@app.route('/salvarContasPagar', methods=['POST',])
def salvarContasPagar():
        
    conta = request.form['conta']
    valor = request.form['valor']
    data = request.form['data']
    
    contas = ContasPagar(conta,valor,data,idcliente=idcliente)
    contas_dao.salvar(contas)
    flash(' Conta Cadastrada com sucesso!','sucesso')
    return redirect('/contas_pagar')



@app.route('/contas_receber')
def contas_receber():
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=index')
   
    return render_template('contas_receber.html', titulo = "Cadastrar conta a receber")

@app.route('/salvarContasReceber', methods=['POST',])
def salvarContasReceber():
        
    tipo = request.form['tipo']
    valor = request.form['valor']
    data = request.form['data']
    
    receber = ContasReceber(tipo,valor,data,idcliente=idcliente)
    receber_dao.salvar(receber)
    flash(' Conta Cadastrada com sucesso!','sucesso')
    return redirect('/contas_pagar')

@app.route('/visualizar_receber')
def visualizar_receber():
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=index')
    lista = receber_dao.listar(idcliente)
   
    return render_template('visualizar_receber.html', titulo = "Cadastre suas Contas a Pagar", recebimento = lista)

@app.route('/visualizar_pagamentos')
def visualizar_pagamentos():
    if 'usuario_logado' not in session or session['usuario_logado']==None:
        return redirect('/login?proxima=index')
    lista = contas_dao.listar(idcliente)
   
    return render_template('visualizar_pagamentos.html', titulo = "Cadastre suas Contas a Pagar", pagamento = lista)


  

#--------------------------------------------------------
if __name__ == 'main':
    port = int(os.getenv('PORT'), '5000')
    app.run(debug=True,host='0.0.0.0', port = port)
     

    
    
    
     
 

 
