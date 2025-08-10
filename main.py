import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0ODM2MDM5LCJpYXQiOjE3NTQ4MzUwMTksImp0aSI6IjE1M2JjYzBmNDA0NDRiZTk5ZmQyZDM5ZjU0YWNiODM4IiwidXNlcl9pZCI6IjEifQ.GRmTKpT-9LlDRLZiu0JGw7Yvi_n0bKuPjTw4ApgfaPo"

url = "http://127.0.0.1:8000/user/me/"  # замени на реальный адрес API

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Текущий пользователь:")
    print(response.json())
else:
    print(f"Ошибка {response.status_code}: {response.text}")
