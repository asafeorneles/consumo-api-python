import requests

url = 'https://viacep.com.br/ws/'
uf = 'MG'
cidade= 'Belo Horizonte'
rua = 'Rua dos Aimores'
formato = '/xml/'

r = requests.get(url + uf + '/' + cidade + '/' + rua + formato)

if (r.status_code == 200):
 print()
 print('XML : ', r.text)
 print()
 
else:
 print('Nao houve sucesso na requisicao.')