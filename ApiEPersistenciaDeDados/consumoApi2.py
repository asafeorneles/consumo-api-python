import requests

url = 'https://api.hgbrasil.com/finance/quotations?key=99ae0dd6'

formato = '/jason/'

r = requests.get(url + formato)

if (r.status_code == 200):
    print()
    print('JASON: ', r.json())
    print()
else:
    print('Nao houve sucesso na requisicao.')