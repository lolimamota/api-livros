from flask import Flask, request, jsonify, render_template

import sqlite3
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    author TEXT NOT NULL,
                    image_url TEXT NOT NULL
                    )""")
    print("Banco de dados criado!")


init_db()


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route('/donate', methods=['POST'])
def donate():
    data = request.get_json()
    title = data.get("title")
    category = data.get("category")
    author = data.get("author")
    image_url = data.get("image_url")

    # if not title or not category or not author or not image_url:

    # if not all([title, category, author, image_url]): outra forma de escrever o comando acima para pegar todos os itens da tabela e dar a ordem abaixo.
    if not all([title, category, author, image_url]):
        return jsonify({'erro': "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect('database.db') as conn:
        conn.execute("""INSERT INTO livros(title,category,author,image_url) VALUES (? , ? , ? , ?)
                    """, (title, category, author, image_url))
        conn.commit()

        return jsonify({'mensagem': "Livro cadastrado com sucesso!"}), 201


@app.route('/donatedBooks', methods=['GET'])
def show_books():
    with sqlite3.connect('database.db') as conn:
        books = conn.execute("SELECT * FROM livros").fetchall()

    formatedBooks = []

    for book in books:
        dictionaryBooks = {
            "id": book[0],
            "title": book[1],
            "category": book[2],
            "author": book[3],
            "image_url": book[4]
        }
        formatedBooks.append(dictionaryBooks)
    return jsonify(formatedBooks)


@app.route('/delete/<int:id>', methods=['DELETE'])
def exclude_book(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (id, ))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"erro": "Este livro existe?"}), 400

    return jsonify({"mensage": "Retiramos este livro da base!"}), 200


@app.route('/update/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    title = data.get("title")
    category = data.get("category")
    author = data.get("author")
    image_url = data.get("image_url")

    if title and not isinstance(title, str):
        return jsonify({"erro": "O campo 'title' deve ser uma string"}), 400

    if category and not isinstance(category, str):
        return jsonify({"erro": "O campo 'category' deve ser uma string"}), 400
    
    if author and not isinstance(author, str):
        return jsonify({"erro": "O campo 'author' deve ser uma string"}), 400
    
    if image_url and not isinstance(image_url, str):
        return jsonify({"erro": "O campo 'image_url' deve ser uma string"}), 400

    if not any([title, category, author, image_url]):
        return jsonify({'erro': "É necessario ter pelo menos um campo para atualizar!"}), 400

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        updates = []
        parameters = []
        if title:
            updates.append("title = ?")
            parameters.append(title)
        if category:
            updates.append("category = ?")
            parameters.append(category)
        if author:
            updates.append("author = ?")
            parameters.append(author)
        if image_url:
            updates.append("image_url = ?")
            parameters.append(image_url)

        if not updates:
            return jsonify({'erro': "Nenhum dado foi fornecido para atualizar"}), 400

        parameters.append(id)

        update_dados = f"UPDATE livros SET {','.join(updates)} WHERE id = ?"
        cursor.execute(update_dados, parameters)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'erro': "Tem certeza sobre o que mudou? Não vi nada!"}), 404
    return jsonify({'mensagem': "Agora confiamos que está tudo certo!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
