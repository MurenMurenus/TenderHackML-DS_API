import requests

print(requests.post('127.0.0.1:5000/api/get_all_purchases/', data={}).json())