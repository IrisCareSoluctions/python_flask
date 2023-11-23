from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle
from datetime import datetime

class Teste:
    def __init__(self, id_teste, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento):
        self.id_teste = id_teste
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
    sql += 'FROM TB_IC_TESTE ORDER BY nome'

    cursor.execute(sql)

    result = cursor.fetchall()

    lista_testes = {}

    for i, row in enumerate(result):
        teste = Teste(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        lista_testes[row[0]] = teste


    sql = "SELECT l.id_log, l.id_teste, l.responsavel, l.dt_hora_exec, l.resultado, l.obs_falha, t.nome, t.desc_procedimento "
    sql += 'FROM TB_IC_TESTE_LOG l INNER JOIN TB_IC_TESTE t ON(l.ID_TESTE = t.ID_TESTE)'

    cursor.execute(sql)

    result = cursor.fetchall()

    lista_log = {}

    for i, row in enumerate(result):
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
    if nome is None:
        nome = ''
    objetivo = data['objetivo']
    if objetivo is None:
        objetivo = ''
    ind_funcional = data['ind_funcional']
    if ind_funcional is None:
        ind_funcional = ''
    preparacao = data['preparacao']
    if preparacao is None:
        preparacao = ''
    dados_input = data['dados_input']
    if dados_input is None:
        dados_input = ''
    dados_output = data['dados_output']
    if dados_output is None:
        dados_output = ''
    desc_procedimento = data['desc_procedimento']
    if desc_procedimento is None:
        desc_procedimento = ''

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

@app.route("/quality/editar-teste/<int:id>")
def quality_editarTeste(id):

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()


    sql = "SELECT id_teste, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento "
    sql += f'FROM TB_IC_TESTE WHERE id_teste = {id}'

    cursor.execute(sql)

    result = cursor.fetchone()

    teste = Teste(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])

    cursor.close()
    connection.close()

    return render_template("quality_editarTeste.html", teste=teste)

@app.route("/quality/atualizarTeste", methods=['POST'])
def quality_atualizarTeste():

    data = request.form

    id_teste = data['id_teste']
    if id_teste is None:
        id_teste = ''
    nome = data['nome']
    if nome is None:
        nome = ''
    objetivo = data['objetivo']
    if objetivo is None:
        objetivo = ''
    ind_funcional = data['ind_funcional']
    if ind_funcional is None:
        ind_funcional = ''
    preparacao = data['preparacao']
    if preparacao is None:
        preparacao = ''
    dados_input = data['dados_input']
    if dados_input is None:
        dados_input = ''
    dados_output = data['dados_output']
    if dados_output is None:
        dados_output = ''
    desc_procedimento = data['desc_procedimento']
    if desc_procedimento is None:
        desc_procedimento = ''

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = 'UPDATE TB_IC_TESTE '
    sql += f"SET NOME = '{nome}', "
    sql += f"OBJETIVO = '{objetivo}', "
    sql += f"IND_FUNCIONAL = '{ind_funcional}', "
    sql += f"PREPARACAO = '{preparacao}', "
    sql += f"DADOS_INPUT = '{dados_input}', "
    sql += f"DADOS_OUTPUT = '{dados_output}', "
    sql += f"DESC_PROCEDIMENTO = '{desc_procedimento}' "
    sql += f"WHERE ID_TESTE = '{id_teste}'"

    cursor.execute(sql)

    connection.commit()

    cursor.close()
    connection.close()

    flash("Ação efetuada com sucesso")

    return redirect(url_for('quality_listarTestes'))

@app.route("/quality/deletarTeste/<int:id>")
def quality_deletarTeste(id):
    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = f'DELETE TB_IC_TESTE WHERE ID_TESTE = {id}'

    cursor.execute(sql)

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('quality_listarTestes'))

@app.route("/quality/listar-testes", methods=['GET'])
def quality_listarTestes():
    
    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = "SELECT id_teste, nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento "
    sql += 'FROM TB_IC_TESTE  ORDER BY id_teste'

    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    lista_testes = {}

    for row in result:
        teste = Teste(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        lista_testes[row[0]] = teste

    return render_template("quality_listarTestes.html", lista_testes=lista_testes)

@app.route("/quality/log-testes", methods=['GET'])
def quality_logTestes():

    connection = cx_Oracle.connect(username, password, dsn)

    cursor = connection.cursor()

    sql = "SELECT l.id_log, l.id_teste, l.responsavel, l.dt_hora_exec, l.resultado, l.obs_falha, t.nome, t.desc_procedimento "
    sql += 'FROM TB_IC_TESTE_LOG l INNER JOIN TB_IC_TESTE t ON(l.ID_TESTE = t.ID_TESTE) ORDER BY dt_hora_exec'

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
    sql += 'FROM TB_IC_TESTE  ORDER BY nome'

    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    lista_testes = {}

    for row in result:
        teste = Teste(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        lista_testes[row[0]] = teste

    return render_template("quality_cadastroLogTestes.html", lista_testes=lista_testes)

@app.route("/quality/cadastrar-log-teste", methods=['POST'])
def quality_cadastrarLogTeste():
    data = request.form

    responsavel = data['responsavel']
    if responsavel is None:
        responsavel = ''
    resultado = data['resultado']
    if resultado is None:
        resultado = ''
    obs_falha = data['obs_falha']
    if obs_falha is None:
        obs_falha = ''
    id_teste = data['nome_teste']
    if id_teste is None:
        id_teste = ''

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