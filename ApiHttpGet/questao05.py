import requests

r = requests.get('http://www.google.com/search', params={'q': 'elson de abreu'})

if (r.status_code == 200):
 arquivo = open('resultado.html', 'w', encoding='utf-8')
 arquivo.write(r.text)
 arquivo.close()

else:
 print('Nao houve sucesso na requisicao.')
