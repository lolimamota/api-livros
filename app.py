from flask import Flask, request, jsonify;

import sqlite3;

app = Flask(__name__)

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
    return '<h2>Acredite, foi iniciado um banco de dados aqui!</h2>';


@app.route('/donate', methods=['POST'])
def donate():
    data = request.get_json()
    title = data.get("title")
    category = data.get("category") 
    author = data.get("author")
    image_url = data.get("image_url")

    if not title or not category or not author or not image_url:
    
    # if not all([title, category, author, image_url]): outra forma de escrever o comando acima para pegar todos os itens da tabela e dar a ordem abaixo.

        return jsonify({'erro': "Todos os campos são obrigatórios"}), 400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute(f"""INSERT INTO livros(title,category,author,image_url) VALUES (?, ? , ? , ?)
                    """, (title, category, author, image_url))
        conn.commit()

        return jsonify({'mensagem': "Livro cadastrado com sucesso!"}), 201

if __name__ == '__main__':
    app.run(debug=True)