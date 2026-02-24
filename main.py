from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Configuração inicial do Banco de Dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nota REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alunos')
def listar_alunos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome, nota FROM alunos')
    alunos = [{"nome": row[0], "nota": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(alunos)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.get_json()
    nome = dados.get('nome')
    nota = dados.get('nota')
    
    if nome and nota is not None:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO alunos (nome, nota) VALUES (?, ?)', (nome, nota))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso"}), 201
    return jsonify({"status": "erro"}), 400

if __name__ == '__main__':
    init_db()
    # O host 0.0.0.0 é essencial para o Replit funcionar
    app.run(host='0.0.0.0', port=81)
