import requests
import uuid
import json
import random

host = "http://0.0.0.0:8000"


class Auth:
    username = None
    password = None
    token = None

    def __init__(self, username, password):
        self.username = username
        self.password = password
        return

    def do_signup(self):
        print("signup: start")
        params = {"username": self.username, "password": self.password}
        response = requests.post(f"{host}/am/signup", params=params)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                pass
        print("signup: done")
        return

    def do_signin(self):
        print("signin: start")
        params = {"username": self.username, "password": self.password}
        response = requests.post(f"{host}/am/signin", params=params)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                self.token = response_json["token"]
                print("token:", self.token)
        print("signin: done")
        return


class Notebook:
    user = None
    notes = None 
    def __init__(self, user):
        self.user = user
        return
    
    def get(self):
        print("notebook get: start")
        params = {"username": self.user.username, "token": self.user.token}
        response = requests.post(f"{host}/notebook/get", params=params)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                self.notes = response_json["notes"]
                print(response_json["notes"])
        print("notebook get: done")
        return

    def delete(self, note_id):
        print("notebook delete: start")
        print(note_id)
        params = {"username": self.user.username, "token": self.user.token}
        data = {"note_id": note_id}
        response = requests.post(f"{host}/notebook/delete", params=params, data=json.dumps(data))
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                pass
        print("notebook delete: done")
        return
    
    def add(self):
        print("notebook add: start")
        params = {"username": self.user.username, "token": self.user.token}
        response = requests.post(f"{host}/notebook/add", params=params)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                pass
        print("notebook add: done")
        return
    
    def update(self, note):
        print("notebook update: start")
        params = {"username": self.user.username, "token": self.user.token}
        data = {
            "note_id": note["note_id"], "title": note["title"],
            "text": note["text"], "checked": note["checked"]
        }
        response = requests.post(f"{host}/notebook/update", params=params, data=json.dumps(data))
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                pass
        print("notebook update: done")
        return


username, password = uuid.uuid4().hex[:15], uuid.uuid4().hex
print("auth data:", username, password)

auth = Auth(username, password)
auth.do_signup()
auth.do_signin()
notebook = Notebook(auth)
notebook.get()
notebook.add()
notebook.add()
notebook.get()
notebook.update({"note_id": random.choice(list(notebook.notes.keys())), "text": "...", "title": "......", "checked": True})
notebook.get()
notebook.delete(random.choice(list(notebook.notes.keys())))
notebook.get()
