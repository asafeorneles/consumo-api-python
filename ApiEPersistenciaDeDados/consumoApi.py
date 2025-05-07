import requests
import json
import sqlite3
from datetime import datetime


url = 'https://api.hgbrasil.com/finance?format=json-cors&key=99ae0dd6'

r = requests.get(url)

if (r.status_code == 200):
    print()
    dados = r.json()
    print('JASON: ', json.dumps(dados, indent=4))
    print()

    dolar = dados['results']['currencies']['USD']['buy']
    euro = dados['results']['currencies']['EUR']['buy']

    print('Cotação do Dólar: R$', dolar)
    print('Cotação do Euro: R$', euro)

    con = sqlite3.connect('bdcotacoes.db')
    cursor = con.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moedas (
            data TEXT,
            dolar REAL,
            euro REAL
        )
    ''')
    con.commit()

    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO moedas (data, dolar, euro)
        VALUES (?, ?, ?)
    ''', (data, dolar, euro))

    con.commit()
    con.close()

else:
    print('Nao houve sucesso na requisicao.')
