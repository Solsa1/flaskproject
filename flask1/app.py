import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.abspath(os.path.dirname(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Prato(db.Model):
    nome = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    preco = db.Column(db.Float, unique=False, nullable=False, primary_key=False)
    desc = db.Column(db.String(100), unique=True, nullable = False, primary_key=False)

    def __repr__(self):
        return f"<Nome: {self.nome}>\n<Preco: {self.preco}>\n<Desc: {self.desc}>"
    

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
    pratos = None
    if request.method == "POST":
        nome = request.form["nome"]
        preco = request.form["preco"]
        desc = request.form.get("desc")
        if nome and preco and desc:  # Verifica se o título não está vazio
            try:
                nome = Prato(nome=nome)
                preco = Prato(preco=preco)
                desc = Prato(desc=desc)
                db.session.add(nome)
                db.session.add(preco)
                db.session.add(desc)
                db.session.commit()
            except Exception as e:
                db.session.rollback()  # Faz o rollback para evitar a sessão pendente
                print("Erro em registrar livro:", e)
        else:
            print("Erro: Título do livro não pode estar vazio.")
    pratos = Prato.query.all()
    return render_template("index.html", pratos=pratos)

@app.route("/update", methods=["POST"])
def update():
    try:
        novoNome = request.form.get("novoNome")
        antigoNome = request.form.get("antigoNome")
        novoPreco = request.form.get("novoPreco")
        antigoPreco = request.form.get("antigoPreco")
        novoDesc = request.form.get("novoDesc")
        antigoDesc = request.form.get("antigoDesc")
        prato = Prato.query.filter_by(nome=antigoNome).first()
        prato.nome = novoNome
        prato.preco = novoPreco
        prato.desc = novoDesc
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Não foi possível atualizar o livro:", e)
    return redirect("/")
'''
@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    try:
        book = Book.query.filter_by(title=title).first()
        if book:
            db.session.delete(book)
            db.session.commit()
        else:
            print("Erro: Livro não encontrado.")
    except Exception as e:
        db.session.rollback()
        print("Não foi possível deletar o livro:", e)
    return redirect("/")
'''
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
