from fastapi import APIRouter, Depends
from app.schemas.routing_intents_handlers import Item
from app.services.routing_intents_handlers import RoutingIntentHendlerService
from app.services.users_auth import current_active_user
from app.db.db import User

router = APIRouter(
    prefix="/handle-events",
    tags=["Events"],
)
events_handler_router = dict(router=router)


@router.post("")
async def handle_events(event_item: Item, user: User = Depends(current_active_user)):
    return await RoutingIntentHendlerService.handle_events(event_item)
