import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.abspath(os.path.dirname(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
    books = None
    if request.method == "POST":
        title = request.form.get("title")
        if title:  # Verifica se o título não está vazio
            try:
                book = Book(title=title)
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                db.session.rollback()  # Faz o rollback para evitar a sessão pendente
                print("Erro em registrar livro:", e)
        else:
            print("Erro: Título do livro não pode estar vazio.")
    books = Book.query.all()
    return render_template("index.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        novotitulo = request.form.get("novotitulo")
        tituloantigo = request.form.get("tituloantigo")
        book = Book.query.filter_by(title=tituloantigo).first()
        book.title = novotitulo
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Não foi possível atualizar o livro:", e)
    return redirect("/")

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
