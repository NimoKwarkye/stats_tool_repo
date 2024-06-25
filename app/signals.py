from enum import Enum, auto
from typing import Callable


class Event(Enum):
    EVENT_NOT_REGISTERED = auto()
    SHOW_APP_UI = auto()



registered_events : dict[Event, list[Callable]]

def register(event:Event, func:Callable):
    global registered_events
    if event in registered_events:
        registered_events[event].append(func)
    else:
        registered_events[event] = [func]

def emit(event:Event, **kwargs):
    if event in registered_events:
        for fn in registered_events[event]:
            fn(**kwargs)
    else:
        emit(Event.EVENT_NOT_REGISTERED)