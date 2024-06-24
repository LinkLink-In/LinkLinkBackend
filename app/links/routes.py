from fastapi import APIRouter

from .schemas import LinkRead, LinkCreate, LinkUpdate

router = APIRouter(
    prefix='/links',
    tags=['links']
)


@router.get('/{short_id}', response_model=LinkRead)
async def get_link(short_id: str):
    pass


@router.post('/create', response_model=LinkRead)
async def create_link(link: LinkCreate):
    pass


@router.post('/{banner_id}', response_model=LinkRead)
async def update_link(short_id: str, link: LinkUpdate):
    pass


@router.get('/list', response_model=list[LinkRead])
async def list_links():
    pass
