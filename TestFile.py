import requests
import json
from flask import jsonify

BASE = "http://127.0.0.1:8000/"

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6InFCYzZEWDRkTWNOME9YX2NoMTUyT2Z2THR2YUVXWjQ3QVJLeHVoQ2JtWG8ifQ.eyJpZGVudGl0eSI6ImIyNTkwMTYyIiwiaXNzIjoiaHR0cDovL2lkcGludGVybmFsLWNlcnQuY29ycGNlcnQuaGViLmNvbS9hZGZzL3NlcnZpY2VzL3RydXN0IiwiYXVkIjpbIm1pY3Jvc29mdDppZGVudGl0eXNlcnZlcjowMTc5ZDQ2ZS02ZmMyLTRmZGMtYWNlZS01NTE0ZDZlNTVhNWYiXSwic3ViIjoiYjI1OTAxNjIiLCJleHAiOjE2MjU2ODQ0Mzd9.ON9VucQFzLnggN4A3FeZACG27TSPWzDOhub7tDuQY-RLQTY1LJTsWOeXC2ICmhmJpdOGe8k3OZP2n-zqNrZny6-kKFiHQIzs9hpSLXq9ulLIsKg8igCZeSLX_aBLvL1uNMfQP3ugsl3H3hRdPboIMnqC2nJoTn3MqDNxKnlUMCMS2-YwwNTM-92vahVr2_TJjmrbxnyvK5Q6XI0_-TUzGTuiN8c9zQ0Z-zi7j7w3UEAtISOTq0va8tuMz1f3fJNTGpOj_uZfC1pbljZorFlof1ploHszAsbwnVwSv9BpwkGruHATLtEP2UrmCvne7loaiQuCAcLvrsOz7_499bGgbQ"
}


data = {
    "username": "NotAGamer3",
    "email": "gmail@gmail.com",
    "first_name": "John",
    "last_name": "Smith",
    "password": "realPassword",
    "phone": "2107654321"
}
work = json.dumps(data)
response = requests.put(
    f"http://127.0.0.1:5000/users/register/{work}", data=data, headers=headers
)
print(response)

data = {
    "username": "NotAGamer3",
    "password": "fakePassword"
}
work = json.dumps(data)
response = requests.post(
    f"http://127.0.0.1:5000/users/login/NotAGamer3/fakePassword", headers=headers
)
print(response)

# response = requests.get("http://127.0.0.1:8000/admin/users/")
# print(response.json())
