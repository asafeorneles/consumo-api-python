from flask import Flask
from flask import request
from flask import render_template
from datetime import date
import sqlite3
from sqlite3 import Error

#######################################################
# Instancia da Aplicacao Flask
app = Flask(__name__)
#######################################################

import os

def criar_tabela():
    try:
        os.makedirs('database', exist_ok=True)  # <- Garante que a pasta exista
        conn = sqlite3.connect('database/db-produtos.db')
        sql = '''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                precocompra REAL NOT NULL,
                precovenda REAL NOT NULL,
                datacriacao DATE NOT NULL
            )
        '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Error as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        if 'conn' in locals():  # <- evita erro se a conexão falhar
            conn.close()

@app.route('/')
def home():
    return render_template('index.html')  # Crie esse HTML ou redirecione


# 1. Cadastrar produtos
@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        datacriacao = date.today()
        mensagem = 'Erro - nao cadastrado'

        if descricao and precocompra and precovenda and datacriacao:
            registro = (descricao, precocompra, precovenda, datacriacao)
            try:
                conn = sqlite3.connect('database/db-produtos.db')
                sql = '''
                    INSERT INTO produtos(descricao, precocompra, precovenda, datacriacao)
                    VALUES(?,?,?,?)
                '''
                cur = conn.cursor()
                cur.execute(sql, registro)
                conn.commit()
                mensagem = 'Sucesso - cadastrado'
            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('cadastrar.html')

#######################################################
# 2. Listar produtos
@app.route('/produtos/listar', methods=['GET'])
def listar():
    try:
        conn = sqlite3.connect('database/db-produtos.db')
        sql = '''SELECT * FROM produtos'''
        cur = conn.cursor()
        cur.execute(sql)
        registros = cur.fetchall()
        return render_template('listar.html', regs=registros)
    except Error as e:
        print(e)
    finally:
        conn.close()

#######################################################
# Rota de Erro
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

#######################################################

# 3. Atualizar produto
@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    try:
        conn = sqlite3.connect('database/db-produtos.db')
        cur = conn.cursor()

        if request.method == 'POST':
            descricao = request.form['descricao']
            precocompra = request.form['precocompra']
            precovenda = request.form['precovenda']

            sql = '''
                UPDATE produtos
                SET descricao = ?, precocompra = ?, precovenda = ?
                WHERE id = ?
            '''
            cur.execute(sql, (descricao, precocompra, precovenda, id))
            conn.commit()
            return "Produto atualizado com sucesso! <a href='/produtos/listar'>Voltar</a>"

        else:
            sql = '''SELECT * FROM produtos WHERE id = ?'''
            cur.execute(sql, (id,))
            produto = cur.fetchone()
            return render_template('editar.html', produto=produto)
    except Error as e:
        return f"Erro ao editar: {e}"
    finally:
        conn.close()

 # 4. Deletar produto
@app.route('/produtos/deletar/<int:id>', methods=['POST'])
def deletar(id):
    try:
        conn = sqlite3.connect('database/db-produtos.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM produtos WHERE id = ?', (id,))
        conn.commit()
        return "Produto deletado com sucesso! <a href='/produtos/listar'>Voltar</a>"
    except Error as e:
        return f"Erro ao deletar: {e}"
    finally:
        conn.close()
       

# Execucao da Aplicacao
if __name__ == '__main__':
    criar_tabela()
    app.run()

