from typing import Optional
from fastapi import FastAPI, Request, Query, Depends, Body
from fastapi.middleware.cors import CORSMiddleware

from todos.components import config, connect
from todos.components.Notebook import Notebook
from todos.components.User import User

from todos.models import User as UserModels
from todos.models import Notebook as NotebookModels


app = FastAPI(debug=True)
app.title = config.app_title
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "https://github.com/rustzz/todos"


@app.post("/am/signup")
async def am_signup(user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    return await _user.signup()


@app.post("/am/signin")
async def am_signin(user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    return await _user.signin()


@app.post("/notebook/add")
async def notebook_add(user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    _notebook = Notebook((connect, config), user=user)

    if not await _user.user_exists():
        return {"status": False}
    if not await _user.is_valid_token():
        return {"status": False}
    return await _notebook.add()


@app.post("/notebook/update")
async def notebook_update(data: NotebookModels.DataNotebook, user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    _notebook = Notebook((connect, config), user=user, data=data)

    if not await _user.user_exists():
        return {"status": False}
    if not await _user.is_valid_token():
        return {"status": False}
    return await _notebook.update()


@app.post("/notebook/delete")
async def notebook_delete(data: NotebookModels.DataNotebook, user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    _notebook = Notebook((connect, config), user=user, data=data)
            
    if not await _user.user_exists():
        return {"status": False}
    if not await _user.is_valid_token():
        return {"status": False}
    return await _notebook.delete()


@app.post("/notebook/get")
async def notebook_get(user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    _notebook = Notebook((connect, config), user=user)

    if not await _user.user_exists():
        return {"status": False, "reason": "Данного имени пользователя не существует"}
    if not await _user.is_valid_token():
        return {"status": False, "reason": "Токен не верный"}
    return await _notebook.get()


@app.post("/am/check/token_valid")
async def am_check_token(user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    return {"status": await _user.is_valid_token()}


@app.post("/am/check/user_exists")
async def am_check_user_exists(user: UserModels.User = Depends()):
    _user = User((connect, config), user=user)
    return {"status": await _user.user_exists()}
