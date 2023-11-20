from flask import Flask, render_template, request, redirect, url_for, flash
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

teste1 = Teste('exemplo de nome 1', 'testar o exemplo 1', 'NF', 'Acessar o site', 'dado de input', 'dados de output', 'desc procediemento')
teste2 = Teste('exemplo de nome 2', 'testar o exemplo 2', 'NF', 'Acessar o site', 'dado de input', 'dados de output', 'desc procediemento')

lista_testes = {
    teste1.nome : teste1,
    teste2.nome : teste2
}
class LogTeste:
    def __init__(self, nome_teste, responsavel, dt_hora_exec, resultado, obs_falha, acao_realizada):
        self.nome_teste = nome_teste
        self.responsavel = responsavel
        self.dt_hora_exec = dt_hora_exec
        self.resultado = resultado
        self.obs_falha = obs_falha
        self.acao_realizada = acao_realizada

log_teste1 = LogTeste('Nome do teste 1', 'Vinicius', '18/11/2023 14:26:02', 'SUCESSO', '', 'desc procediemento')
log_teste2 = LogTeste('Nome do teste 2', 'Vinicius', '18/11/2023 14:26:02', 'FALHA', 'falhou ao tentar acessar a pasta', 'desc procediemento')

lista_log = {
    log_teste1.nome_teste:log_teste1,
    log_teste2.nome_teste:log_teste2
}

app = Flask(__name__)
app.secret_key = 'iris_care'


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

    if ind_funcional == '1':
        ind_funcional = 'F'
    elif ind_funcional == '2':
        ind_funcional = 'NF'

    teste = Teste(nome, objetivo, ind_funcional, preparacao, dados_input, dados_output, desc_procedimento)

    lista_testes[teste.nome] = teste

    flash("Ação efetuada com sucesso")

    return redirect(url_for('quality_listarTestes'))

@app.route("/quality/listar-testes", methods=['GET'])
def quality_listarTestes():

    return render_template("quality_listarTestes.html", lista_testes=lista_testes)


@app.route("/quality/log-testes", methods=['GET'])
def quality_logTestes():

    return render_template("quality_logTestes.html", lista_log=lista_log)

@app.route("/quality/cadastro-log-testes", methods=['GET'])
def quality_cadastroLogTestes():

    return render_template("quality_cadastroLogTestes.html", lista_testes=lista_testes)

@app.route("/quality/cadastrar-log-teste", methods=['POST'])
def quality_cadastrarLogTeste():
    data = request.form

    nome_teste = data['nome_teste']
    responsavel = data['responsavel']
    resultado = data['resultado']
    obs_falha = data['obs_falha']

    if resultado == '1':
        resultado = 'SUCESSO'
    elif resultado == '2':
        resultado = 'FALHA'

    data_hora_atual = datetime.now()

    # Formata a data e hora no formato desejado
    formato_desejado = "%d/%m/%Y %H:%M:%S"
    dt_hora_exec = data_hora_atual.strftime(formato_desejado)

    acao_realizada = lista_testes.get(nome_teste).desc_procedimento

    log_teste = LogTeste(nome_teste, responsavel, dt_hora_exec, resultado, obs_falha, acao_realizada)

    lista_log[log_teste.nome_teste] = log_teste

    flash("Ação efetuada com sucesso")

    return redirect(url_for('quality_logTestes'))

app.run(debug=True)