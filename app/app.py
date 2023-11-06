from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from .routers import members
from .prisma import prisma

app = FastAPI()
# app.include_router(members.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def index(request:Request):
    # At a minimum, you must pass the request in the context
    context = {"request":request}
    return templates.TemplateResponse('index.html', context)

@app.get('/login')
async def login(request:Request):
    context = {"request":request}
    return templates.TemplateResponse('login.html', context)

@app.post("/submit")
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
    await prisma.member.create(data={'username': username, 'password': password, "email": 'eadfasd'})
    res = await prisma.member.find_many()
    context = {"request":request}
    return templates.TemplateResponse('submit.html', context)

@app.get('/register')
async def regis(request:Request):
    context = {"request":request}
    return templates.TemplateResponse('register.html', context)

@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
