import fastapi

from . import card

router = fastapi.APIRouter()
router.include_router(router=card.router)
