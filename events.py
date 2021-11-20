from abc import ABC, abstractmethod
from enum import Enum


class EventType(Enum):
    ON_DEATH = 1


class EventListener(ABC):
    @abstractmethod
    def update(self, data):
        pass


class EventManager:
    def __init__(self):
        self.listeners = {EventType.ON_DEATH: []}

    def subscribe(self, event_type: EventType, listener: EventListener):
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type: EventType, listener: EventListener):
        self.listeners[event_type].remove(listener)

    def notify(self, event_type: EventType, data):
        for listener in self.listeners[event_type]:
            listener.update(data)



