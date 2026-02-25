import sqlite3
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuração do caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'alunos.db')

def git_push_db():
    """Função para automatizar o salvamento no GitHub"""
    try:
        # Configura o git (ajuste com seu nome/email se necessário)
        subprocess.run(["git", "config", "user.email", "bot@replit.com"], check=False)
        subprocess.run(["git", "config", "user.name", "Replit Bot"], check=False)
        
        # Comandos de push
        subprocess.run(["git", "add", "alunos.db"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update: alteração no banco de dados"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Dados sincronizados com o GitHub!")
    except Exception as e:
        print(f"⚠️ Erro ao sincronizar com GitHub: {e}")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela se não existir ao iniciar
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM alunos').fetchall()
    conn.close()
    return render_template('index.html', alunos=alunos)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    
    if nome and email:
        conn = get_db_connection()
        conn.execute('INSERT INTO alunos (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        conn.close()
        
        # SALVAMENTO AUTOMÁTICO
        git_push_db()
        
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM alunos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    # SALVAMENTO AUTOMÁTICO
    git_push_db()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
