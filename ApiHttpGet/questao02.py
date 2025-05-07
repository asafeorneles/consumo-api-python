import requests

url = 'https://viacep.com.br/ws/'
cep = 30140071
formato = '/xml/'

for i in range(5):
 cepAtual = str(cep + i)
 r = requests.get(url + cepAtual + formato)

 if (r.status_code == 200):
  print()
  print('XML : ', r.text)
  print()
  
 else:
  print('Nao houve sucesso na requisicao.')