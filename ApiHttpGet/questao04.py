import requests

url = 'https://viacep.com.br/abc/'
cep = '30140071'
formato = '/xml/'

r = requests.get(url + cep + formato)
print()
print('Codigo de retorno: ', r.status_code, '\n')
print('Texto: ', r.text)