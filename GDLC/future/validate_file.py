import requests
import json 

w3cURL = 'https://validator.w3.org/nu/?out=json'
errors = []
payload = open(filepath)
with open(filepath,'rb') as payload:
      headers = {'content-type': 'text/html; charset=utf-8', 'Accept-Charset': 'UTF-8'}
      r = requests.post(w3cURL, data=payload, headers=headers)
      errors = r.json()['messages']
