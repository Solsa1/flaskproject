from flask import *
from filme import *

app = Flask(__name__)

catalogo = []

@app.route('/')
def index():
    return render_template('index.html', catalogo=catalogo)

@app.route('/criar', methods=['POST']) 
def create():
    filme1 = filme()
    filme1.setNome(request.form['nome'])
    filme1.setAutor(request.form['autor'])
    filme1.setDesc(request.form['descricao'])
    catalogo.append(filme1)
    return redirect('/')

@app.route('/alterar', methods=['POST']) # Rota /alterar
def update():
    nome_antigo = request.form['nome_antigo']
    nome_novo = request.form['nome_novo']
    autor_novo = request.form['autor_novo']
    desc_nova = request.form['desc_nova']
    for i in catalogo:
        if i.getNome() == nome_antigo:
            i.setNome(nome_novo)
            i.setAutor(autor_novo)
            i.setDesc(desc_nova)
    return redirect('/')

@app.route('/apagar', methods=['POST']) # Rota /apagar
def delete():
    nome = request.form['nome']
    for i in catalogo:
        if i.getNome() == nome:
            catalogo.remove(i)
            return redirect('/')
    else:
        return "filme inexistente"
if __name__ == '__main__':
    app.run(debug=True)