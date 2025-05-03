from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Self
import asyncio
import re

from state import State

class Command(ABC):
    # TODO: create error sum type
    @abstractmethod
    async def execute(self, State) -> None:
        pass

class SymbolCommandTy(Enum):
    # Start/continue buying
    Start = 0
    # Stop buying
    End = 1
    # Sell all assets and stop
    Kill = 2

# Commands that act on stock symbols
class SymbolCommand(Command):
    exchange: str
    symbol: str
    ty: SymbolCommandTy

    def __init__(self, exchange: str, symbol: str, ty: SymbolCommandTy) -> None:
        self.symbol = symbol
        self.ty = ty

    async def execute(self, state: State) -> None:
        pass

def symbol_command_parser(command: str) -> None | Command:
    match re.match(r"(\w+)/(\w+)@(\w+)", command):
        case re.Match() as matches:
            (ty, symbol, exchange) = matches.group(1, 2, 3)

            match ty:
                case "start":
                    return SymbolCommand(exchange, symbol, SymbolCommandTy.Start)
                case "end":
                    return SymbolCommand(exchange, symbol, SymbolCommandTy.End)
                case "kill":
                    return SymbolCommand(exchange, symbol, SymbolCommandTy.Kill)

    return None

COMMAND_PARSERS: list[Callable[[str], None | Command]] = [
    symbol_command_parser
]
