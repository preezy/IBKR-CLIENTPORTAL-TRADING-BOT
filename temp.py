import requests

link = 'https://localhost:5000/v1/portal/trsrv/futures'

r = requests.get(link, params={'symbols':'ES'}, verify=False)

print(r.content)