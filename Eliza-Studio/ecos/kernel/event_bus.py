import asyncio
from typing import Dict, List, Callable, Awaitable

class EventBus:
    """
    A lightweight, in-memory Pub/Sub message broker using asyncio.Queues.
    In a full production cluster, this would be backed by Redis.
    """
    def __init__(self):
        # Maps channel names to a list of asyncio.Queues (one for each subscriber)
        self.channels: Dict[str, List[asyncio.Queue]] = {}

    def subscribe(self, channel: str) -> asyncio.Queue:
        if channel not in self.channels:
            self.channels[channel] = []
        queue = asyncio.Queue()
        self.channels[channel].append(queue)
        return queue

    def unsubscribe(self, channel: str, queue: asyncio.Queue):
        if channel in self.channels and queue in self.channels[channel]:
            self.channels[channel].remove(queue)

    async def publish(self, channel: str, message: dict):
        if channel in self.channels:
            for queue in self.channels[channel]:
                await queue.put(message)

event_bus = EventBus()
