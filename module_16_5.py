from fastapi import FastAPI, Path, Body, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated
from typing import List

app = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True}, debug=True)

templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/', response_class=HTMLResponse)
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.HTML', {'request': request, 'users': users})

@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1)]):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.HTML', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail='User was not found')

@app.post('/users/{username}/{age}', response_class=HTMLResponse)
async def add_user(request: Request, username: Annotated[str, Path()], age: Annotated[int, Path()]):
    new_id = max(u.id for u in users) + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse('users.HTML', {'request': request, 'users': users})

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, user_age: int, user_name: str = Body()) -> str:
    for u in users:
        if u.id == user_id:
            u.username = user_name
            u.age = user_age
            return u
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            return f'{u} delete'
    raise HTTPException(status_code=404, detail='User was not found')
