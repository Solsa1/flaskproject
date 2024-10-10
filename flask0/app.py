from flask import Flask, render_template, request, redirect 

app = Flask(__name__)

filmes=[]

@app.route('/')
def index():
    return render_template('index.html', filmes=filmes)


@app.route('/criar', methods=['POST']) # Rota /criar
def create():
    nome = request.form['nome']
    filmes.append(nome)
    return redirect('/')


@app.route('/alterar', methods=['POST']) # Rota / alterar
def update():
    old_name = request.form['old_name'] 
    new_name = request.form['new_name']
    if old_name in filmes:
        index = filmes.index(old_name)
        filmes[index] = new_name
    return redirect('/')


@app.route('/apagar', methods=['POST']) # Rota /apagar
def delete():
    nome = request.form['nome']
    if nome in filmes:
        filmes.remove(nome)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)