from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle
from datetime import datetime

class Teste:
    def __init__(self, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento):
        self.nome = nome
        self.objetivo = objetivo
        self.ind_funcional = ind_funcional
        self.preparacao = preparacao
        self.dados_input = dados_input
        self.dados_output = dados_output
        self.desc_procedimento = desc_procedimento

class LogTeste:
    def __init__(self, nome_teste, responsavel, dt_hora_exec, resultado, obs_falha, acao_realizada):
        self.nome_teste = nome_teste
        self.responsavel = responsavel
        self.dt_hora_exec = dt_hora_exec
        self.resultado = resultado
        self.obs_falha = obs_falha
        self.acao_realizada = acao_realizada

app = Flask(__name__)
app.secret_key = 'iris_care'

# Substitua os valores entre aspas com suas próprias informações de conexão
username = "rm93613"
password = "150503"
host = "oracle.fiap.com.br"
port = "1521"
service_name = "ORCL"

# Construa a string de conexão
dsn = cx_Oracle.makedsn(host, port, service_name=service_name)


@app.route("/", methods=['GET'])
def index():

    return render_template('home.html')

@app.route("/sobre", methods=['GET'])
def sobre():

    return render_template('sobre.html')

@app.route("/integrantes", methods=['GET'])
def integrantes():

    return render_template('integrantes.html')

@app.route("/quality", methods=['GET'])
def quality_home():

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = "SELECT id_teste, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento "
    sql += 'FROM TB_IC_TESTE'

    cursor.execute(sql)

    result = cursor.fetchall()

    lista_testes = {}

    for row in result:
        teste = Teste(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        lista_testes[row[0]] = teste


    sql = "SELECT l.id_log, l.id_teste, l.responsavel, l.dt_hora_exec, l.resultado, l.obs_falha, t.nome, t.desc_procedimento "
    sql += 'FROM TB_IC_TESTE_LOG l INNER JOIN TB_IC_TESTE t ON(l.ID_TESTE = t.ID_TESTE)'

    cursor.execute(sql)

    result = cursor.fetchall()

    lista_log = {}

    for row in result:
        log = LogTeste(row[6], row[2], row[3], row[4], row[5], row[7])
        lista_log[row[0]] = log


    cursor.close()
    connection.close()

    return render_template("quality_home.html", lista_testes=lista_testes, lista_log=lista_log)


@app.route("/quality/cadasto-teste", methods=['GET'])
def quality_cadastoTeste():

    return render_template("quality_cadastoTeste.html")

@app.route("/quality/cadastrar-teste", methods=['POST'])
def quality_cadastrarTeste():
    data = request.form

    nome = data['nome']
    objetivo = data['objetivo']
    ind_funcional = data['ind_funcional']
    preparacao = data['preparacao']
    dados_input = data['dados_input']
    dados_output = data['dados_output']
    desc_procedimento = data['desc_procedimento']

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = 'INSERT INTO TB_IC_TESTE (id_teste, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento)'
    sql += "VALUES(SEQ_TB_IC_TESTE.NEXTVAL, :1, :2, :3, :4, :5, :6, :7)"

    cursor.execute(sql, (nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento))

    connection.commit()

    cursor.close()
    connection.close()    

    flash("Ação efetuada com sucesso")

    return redirect(url_for('quality_listarTestes'))

@app.route("/quality/listar-testes", methods=['GET'])
def quality_listarTestes():
    
    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = "SELECT id_teste, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento "
    sql += 'FROM TB_IC_TESTE'

    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    lista_testes = {}

    for row in result:
        teste = Teste(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        lista_testes[row[0]] = teste

    return render_template("quality_listarTestes.html", lista_testes=lista_testes)


@app.route("/quality/log-testes", methods=['GET'])
def quality_logTestes():

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = "SELECT l.id_log, l.id_teste, l.responsavel, l.dt_hora_exec, l.resultado, l.obs_falha, t.nome, t.desc_procedimento "
    sql += 'FROM TB_IC_TESTE_LOG l INNER JOIN TB_IC_TESTE t ON(l.ID_TESTE = t.ID_TESTE)'

    cursor.execute(sql)

    result = cursor.fetchall()

    lista_log = {}

    for row in result:
        log = LogTeste(row[6], row[2], row[3], row[4], row[5], row[7])
        lista_log[row[0]] = log


    cursor.close()
    connection.close()

    return render_template("quality_logTestes.html", lista_log=lista_log)

@app.route("/quality/cadastro-log-testes", methods=['GET'])
def quality_cadastroLogTestes():

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = "SELECT id_teste, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento "
    sql += 'FROM TB_IC_TESTE'

    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    lista_testes = {}

    for row in result:
        teste = Teste(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        lista_testes[row[0]] = teste

    return render_template("quality_cadastroLogTestes.html", lista_testes=lista_testes)

@app.route("/quality/cadastrar-log-teste", methods=['POST'])
def quality_cadastrarLogTeste():
    data = request.form

    responsavel = data['responsavel']
    resultado = data['resultado']
    obs_falha = data['obs_falha']
    id_teste = data['nome_teste']

    data_hora_atual = datetime.now()

    # Formata a data e hora no formato desejado
    formato_desejado = "%d/%m/%Y %H:%M:%S"
    dt_hora_exec = data_hora_atual.strftime(formato_desejado)

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = 'INSERT INTO TB_IC_TESTE_LOG (id_log, id_teste, responsavel, dt_hora_exec, resultado, obs_falha) '
    sql += "VALUES(SEQTB_IC_TESTE_LOG.NEXTVAL, :1, :2, TO_DATE(:3, 'DD/MM/YYYY HH24:MI:SS'), :4, :5)"

    cursor.execute(sql, (id_teste, responsavel, dt_hora_exec, resultado, obs_falha))

    connection.commit()

    cursor.close()
    connection.close()    

    flash("Ação efetuada com sucesso")

    return redirect(url_for('quality_logTestes'))

app.run(debug=True)