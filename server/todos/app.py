from fastapi import FastAPI
from . import api
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends

from .components.handlers import UserHandlers
from .components.handlers import NotebookHandlers

from .api.models import UserModels
from .api.models import NotebookModels

from .components.sql import mysql


app = FastAPI(debug=True)
app.title = api.app_title
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "https://github.com/rustzz/todos"


@app.post("/am/signup")
async def am_signup(user: UserModels.UserAuth = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    return await user_handler.signup()


@app.post("/am/signin")
async def am_signin(user: UserModels.UserAuth = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    return await user_handler.signin()


@app.post("/notebook/add")
async def notebook_add(user: UserModels.UserFunc = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    notebook_handler = NotebookHandlers.Notebook(connection=mysql, user=user)

    if not await user_handler.user_exists():
        return {"status": False}
    if not await user_handler.is_valid_token():
        return {"status": False}
    if not bool(user.username) or not bool(user.token):
        return {"status": False, "reason": "Один из параметров имеет <null> тип"}
    return await notebook_handler.add()


@app.post("/notebook/update")
async def notebook_update(data: NotebookModels.DataNotebook, user: UserModels.UserFunc = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    notebook_handler = NotebookHandlers.Notebook(connection=mysql, user=user, data=data)

    if not await user_handler.user_exists():
        return {"status": False}
    if not await user_handler.is_valid_token():
        return {"status": False}
    if not bool(user.username) or not bool(user.token):
        return {"status": False, "reason": "Один из параметров имеет <null> тип"}
    return await notebook_handler.update()


@app.post("/notebook/delete")
async def notebook_delete(data: NotebookModels.DataNotebook, user: UserModels.UserFunc = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    notebook_handler = NotebookHandlers.Notebook(connection=mysql, user=user, data=data)
            
    if not await user_handler.user_exists():
        return {"status": False}
    if not await user_handler.is_valid_token():
        return {"status": False}
    if not bool(user.username) or not bool(user.token):
        return {"status": False, "reason": "Один из параметров имеет <null> тип"}
    return await notebook_handler.delete()


@app.post("/notebook/get")
async def notebook_get(user: UserModels.UserFunc = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    notebook_handler = NotebookHandlers.Notebook(connection=mysql, user=user)

    if not await user_handler.user_exists():
        return {"status": False, "reason": "Данного имени пользователя не существует"}
    if not await user_handler.is_valid_token():
        return {"status": False, "reason": "Токен не верный"}
    if not bool(user.username) or not bool(user.token):
        return {"status": False, "reason": "Один из параметров имеет <null> тип"}
    return await notebook_handler.get()


@app.post("/am/check/token_valid")
async def am_check_token(user: UserModels.UserFunc = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    return {"status": await user_handler.is_valid_token()}


@app.post("/am/check/user_exists")
async def am_check_user_exists(user: UserModels.User = Depends()):
    user_handler = UserHandlers.User(connection=mysql, user=user)
    return {"status": await user_handler.user_exists()}
