import requests

futures = 'https://localhost:5000/v1/portal/trsrv/futures'

stock = 'https://localhost:5000/v1/portal/iserver/secdef/search'

r = requests.post(stock, data={'symbol':'FB'}, verify=False)

print(r.content)