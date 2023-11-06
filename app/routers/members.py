from fastapi import APIRouter
from ..dtos.member import CreateMemberDto
from ..prisma import prisma

router = APIRouter(
    prefix="/member",
    tags=["member"],
    responses={404: {"description": "Not found"}},
)
@router.get('/')
async def fetch_member():
    result = await prisma.member.find_many()
    return result

@router.get('/{id}')
async def fetch_member_id(id: int):
    result = await prisma.member.find_first(where={'id': int(id)})
    return result

@router.post("/createmember")
async def read_root(memberDto: CreateMemberDto):
    await prisma.member.create(data={"username": memberDto.username, "password": memberDto.password, "balance": 0, "email": memberDto.email})
    return {
        'message': 'Sucessfully Create Member'
    }

@router.put('/updatemember/{id}')
async def update_member(id: int, memberDto: CreateMemberDto):
    await prisma.member.update(where={'id': int(id)}, data={"username": memberDto.username, "email": memberDto.email, "password": memberDto.password})
    return {
        'message': 'Sucessfully Updated'
    }

@router.delete("/deletemember/{id}")
async def delete_member(id):
    print(id)
    await prisma.member.delete(where={'id': int(id)})
    return {
        'message': 'Sucessfully Deleted'
    }