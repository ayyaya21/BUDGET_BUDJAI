from fastapi import FastAPI, Request, Form, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from .dtos.task import CreateTransactionDto
from .prisma import prisma
import datetime
import calendar

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def index(request:Request, login: Annotated[bool | None, Cookie()] = None):
    context = {"request":request}
    if login:
        return templates.TemplateResponse('submit.html', context)
    else:
        return templates.TemplateResponse('index.html', context)

@app.get('/login')
async def login(request:Request):
    context = {"request":request}
    return templates.TemplateResponse('login.html', context)

@app.post("/submit")
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
    context = {"request":request}
    if username == 'test' and password == 'password':
        return templates.TemplateResponse('submit.html', context)
    else:
       return templates.TemplateResponse('error.html', context)

@app.get('/home')
async def submit(request:Request, login: Annotated[bool | None, Cookie()] = None):
    transaction = await prisma.transaction.find_many()
    expense = await prisma.transaction.find_many(where={'type': "EXPENSE"})
    expense_total = 0
    for i in expense:
        expense_total += i.money
    income = await prisma.transaction.find_many(where={'type': "INCOME"})
    income_total = 0

    for i in income:
        income_total += i.money
    balance_money = income_total - expense_total

    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    num_days = calendar.monthrange(current_year, current_month)[1]
    days_in_month = [day for day in range(1, num_days + 1)][-1]
    daily = balance_money // days_in_month
    context = {'request':request, 'transaction':transaction, 'show':{
        "income": income_total,
        "expense": expense_total,
        "balance": balance_money,
        "daily": daily
    }}
    if login:
        return templates.TemplateResponse('home.html', context)
    else:
        return templates.TemplateResponse('error.html', context)

#คำนวณทั้งหมด
@app.get('/home')
async def calculate():
    result = await prisma.transaction.find_many()
    expense = await prisma.transaction.find_many(where={'type': "EXPENSE"})
    expense_total = 0
    for i in expense:
        expense_total += i.money
    income = await prisma.transaction.find_many(where={'type': "INCOME"})
    income_total = 0

    for i in income:
        income_total += i.money
    balance_money = income_total - expense_total

    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    num_days = calendar.monthrange(current_year, current_month)[1]
    days_in_month = [day for day in range(1, num_days + 1)][-1]
    daily = balance_money // days_in_month
    return {
        "items": result,
        "income": income_total,
        "expense": expense_total,
        "balance": balance_money,
        "daily": daily
    }

@app.get('/',response_class=HTMLResponse)
async def read_items(request:Request):
    items = ['items', 'income', 'expense', 'balance', 'daily']
    return templates.TemplateResponse('home.html', {'request':request,'items':items})

@app.post('/home')
async def create_transaction(taskdto: CreateTransactionDto):
    await prisma.transaction.create(data={'name': taskdto.name, 'money': float(taskdto.money), 'type': taskdto.type})
    return await prisma.transaction.find_many()

@app.delete('/home')
async def delete_transaction():
    await prisma.transaction.delete_many()
    return await prisma.transaction.find_many()

@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
