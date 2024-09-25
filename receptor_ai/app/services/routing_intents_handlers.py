from functools import reduce
import aiohttp
from app.db.db import db
from app.logger.info_logger import logger


class RoutingIntentHendlerService:
    @staticmethod
    async def call_destination_endpoint_url(url, method, payload=None):
        async with aiohttp.ClientSession() as session:
            try:
                async with (
                    session.get(url)
                    if method == "http.get"
                    else session.post(url, json=payload, ssl=False)
                ) as response:
                    return await response.text()
            except Exception as exc:
                logger.error(f"Exception occurred {url} {method} {payload} {exc}")

    @staticmethod
    def get_destination_strategy_mapping():
        return {
            "ALL": lambda routing_intents: [
                routing_intent.destinationName for routing_intent in routing_intents
            ],
            "IMPORTANT": lambda routing_intents: [
                routing_intent.destinationName
                for routing_intent in routing_intents
                if getattr(routing_intent, "important", False) == True
            ],
            "SMALL": lambda routing_intents: [
                routing_intent.destinationName
                for routing_intent in routing_intents
                if isinstance(bytes := routing_intent.bytes, int) and bytes < 1024
            ],
        }

    @staticmethod
    def get_safe_globals_for_eval():
        return {
            "max": max,
            "min": min,
            "sorted": sorted,
            "reduce": reduce,
            "list": list,
            "__builtins__": None,  # Disable built-ins to prevent dangerous functions from being executed
        }

    @classmethod
    async def handle_events(cls, event):
        destination_strategy_mapping = cls.get_destination_strategy_mapping()
        safe_globals = cls.get_safe_globals_for_eval()
        routing_intents = event.routingIntents
        safe_locals = {
            "routing_intents": routing_intents  # Only pass routing_intents into the lambda
        }
        destinations = []
        strategy = event.strategy
        if strategy.startswith("lambda routing_intents:"):
            strategy_func = eval(strategy, safe_globals, safe_locals)
            destinations = strategy_func(routing_intents)
        else:
            destinations = destination_strategy_mapping.get(strategy)(routing_intents)
        response_destinations = {}
        for destination in destinations:
            record = await db["destinations"].find_one(
                {"destinationName": destination}, {"_id": 0}
            )
            if record:
                response_destinations[destination] = True
                transport = record.get("transport", "")
                if transport in ["http.get", "http.post"]:
                    await cls.call_destination_endpoint_url(
                        url=record.get("url", "http://example.com/endpoint"),
                        method=record.get("transport", "http.get"),
                        payload=event.payload,
                    )

                logger.info(
                    f"payload sent to [{destination}] via {transport} transport"
                )
            else:
                response_destinations[destination] = False
                logger.error(f"UnknownDestinationError ({destination})")
        return response_destinations