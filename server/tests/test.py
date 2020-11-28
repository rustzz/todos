import requests
import uuid
import json
import os
import random
import asyncio


host = f"http://{os.getenv('API_SERVER_HOST')}:{os.getenv('API_SERVER_PORT')}"


class Auth:
    username = None
    password = None
    token = None

    def __init__(self, auth_data):
        self.username = auth_data[0]
        self.password = auth_data[1]
        return

    async def do_signup(self):
        print("signup: start")
        params = {"username": self.username, "password": self.password}
        response = requests.post(f"{host}/am/signup", params=params)
        print(f"[{response.status_code}]")
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                return response_json
        print("signup: done")
        return

    async def do_signin(self):
        print("signin: start")
        params = {"username": self.username, "password": self.password}
        response = requests.post(f"{host}/am/signin", params=params)
        print(f"[{response.status_code}]")
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                self.token = response_json["token"]
                return response_json
        print("signin: done")
        return


class Notebook:
    user = None
    notes = None

    def __init__(self, user):
        self.user = user
        return
    
    async def get(self):
        print("notebook get: start")
        params = {"username": self.user.username, "token": self.user.token}
        response = requests.post(f"{host}/notebook/get", params=params)
        print(f"[{response.status_code}]")
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                self.notes = response_json["notes"]
                return response_json
        print("notebook get: done")
        return

    async def delete(self, note_id):
        print("notebook delete: start")
        params = {"username": self.user.username, "token": self.user.token}
        data = {"id": note_id}
        response = requests.post(f"{host}/notebook/delete", params=params, data=json.dumps(data))
        print(f"[{response.status_code}]")
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                return response_json
        print("notebook delete: done")
        return
    
    async def add(self):
        print("notebook add: start")
        params = {"username": self.user.username, "token": self.user.token}
        response = requests.post(f"{host}/notebook/add", params=params)
        print(f"[{response.status_code}]")
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                return response_json
        print("notebook add: done")
        return
    
    async def update(self, note):
        print("notebook update: start")
        params = {"username": self.user.username, "token": self.user.token}
        data = {
            "id": note["id"], "title": note["title"],
            "text": note["text"], "checked": note["checked"]
        }
        response = requests.post(f"{host}/notebook/update", params=params, data=json.dumps(data))
        print(f"[{response.status_code}]")
        if response.status_code == 200:
            response_json = response.json()
            if "status" in response_json and response_json["status"]:
                return response_json
        print("notebook update: done")
        return


async def start(thread_count):
    for _ in range(thread_count):
        username, password = uuid.uuid4().hex[:15], uuid.uuid4().hex
        print("auth data:", username, password)

        auth = Auth((username, password))
        await auth.do_signup()
        await auth.do_signin()

        notebook = Notebook(auth)
        await notebook.add()
        await notebook.add()
        await notebook.get()
        await notebook.update({
            "id": random.choice(list(notebook.notes.keys())),
            "text": "...",
            "title": "......",
            "checked": True
        })
        await notebook.delete(random.choice(list(notebook.notes.keys())))
    return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    thread_count = int(input("THREADS: "))
    loop.run_until_complete(start(thread_count))
