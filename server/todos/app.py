from typing import Optional
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware

from todos.components import config, connect
from todos.components.Notes import Notes
from todos.components.User import User


app = FastAPI(debug=True)
origins = [
    '*',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def root():
    return 'Документации пока нет'


@app.post('/am/register')
async def am_register(username: str = Query(None, min_length=4, max_length=15),
                      password: str = Query(None, min_length=6, max_length=64)):
    user = User((connect, config), username=username, password=password)
    return await user.register()


@app.post('/am/login')
async def am_login(username: str = Query(None, min_length=4, max_length=15),
                   password: str = Query(None, min_length=6, max_length=64)):
    print(username, password)
    user = User((connect, config), username=username, password=password)
    return await user.login()


@app.post('/notebook/add')
async def notebook_add(username: str = Query(None, min_length=4, max_length=15),
                       token: str = Query(None, min_length=64, max_length=64)):
    user = User((connect, config), username=username, token=token)
    notes = Notes((connect, config), user)

    if not await user.user_exists():
        return {'status': False}
    if not await user.is_valid_token():
        return {'status': False}
    return await notes.add()


@app.post('/notebook/update')
async def notebook_update(data: dict,
                          username: str = Query(None, min_length=4, max_length=15),
                          token: str = Query(None, min_length=64, max_length=64)):
    user = User((connect, config), username=username, token=token)
    notes = Notes((connect, config), user, data=data)

    if not await user.user_exists():
        return {'status': False}
    if not await user.is_valid_token():
        return {'status': False}
    return await notes.update()


@app.post('/notebook/delete')
async def notebook_delete(data: dict,
                          username: str = Query(None, min_length=4, max_length=15),
                          token: str = Query(None, min_length=64, max_length=64)):
    user = User((connect, config), username=username, token=token)
    notes = Notes((connect, config), user, data=data)
            
    if not await user.user_exists():
        return {'status': False}
    if not await user.is_valid_token():
        return {'status': False}
    return await notes.delete()


@app.post('/notebook/get')
async def notebook_get(username: str = Query(None, min_length=4, max_length=15),
                       token: str = Query(None, min_length=64, max_length=64)):
    user = User((connect, config), username=username, token=token)
    notes = Notes((connect, config), user)

    if not await user.user_exists():
        return {'status': False, 'reason': 'Имя пользователя не существует'}
    if not await user.is_valid_token():
        return {'status': False, 'reason': 'Токен не верный'}
    return await notes.get()


@app.post('/am/check/token_valid')
async def am_check_token(username: str = Query(None, min_length=4, max_length=15),
                         token: str = Query(None, min_length=64, max_length=64)):
    user = User((connect, config), username=username, token=token)
    return {'status': await user.is_valid_token()}


@app.post('/am/check/user_exists')
async def am_check_user_exists(username: str = Query(None, min_length=4, max_length=15)):
    user = User((connect, config), username=username)
    return {'status': await user.user_exists()}
