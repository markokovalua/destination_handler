from typing import Union, List, Dict, Literal
from pydantic import BaseModel, field_validator
from app.logger.info_logger import logger

class RoutingIntent(BaseModel):
    destinationName: str  # Required field
    important: bool = None  # Required boolean field
    bytes: int = None  # Required integer field


class Item(BaseModel):
    payload: Union[Dict, None] = None
    routingIntents: List[RoutingIntent]
    strategy: Union[Literal["ALL", "IMPORTANT", "SMALL"], str] = None

    # Validator to check the strategy field
    @field_validator("strategy")
    def validate_strategy(cls, value):
        # Check if the value is one of the allowed strings
        if value is None:
            return value
        if value in ["ALL", "IMPORTANT", "SMALL"]:
            return value
        # Check if it starts with 'lambda routing_intents:'
        if value.startswith("lambda routing_intents:"):
            return value
        msg = "strategy must be one of 'ALL', 'IMPORTANT', 'SMALL', or start with 'lambda routing_intents:'"
        logger.error(msg)
        raise ValueError(msg)

    # Validator to check if payload contains 'destinationName' key when payload is provided
    @field_validator("payload")
    def validate_payload_destination_name(cls, value):
        if value and "destinationName" not in value:
            msg = "strategy must be one of 'ALL', 'IMPORTANT', 'SMALL', or start with 'lambda routing_intents:'"
            logger.error(msg)
            raise ValueError(msg)
        return value
