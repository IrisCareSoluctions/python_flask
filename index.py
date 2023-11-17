from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'iris_care'

@app.route("/", methods=['GET'])
def index():

    return render_template('home.html')

@app.route("/sobre", methods=['GET'])
def sobre():

    return render_template('sobre.html')

app.run(debug=True)