from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Self
import asyncio
import re

from state import State

class Command(ABC):
    # TODO: create error sum type
    @abstractmethod
    async def execute(self, State):
        pass

    @abstractmethod
    def parse(command: str) -> None | Self:
        pass

class SymbolCommandTy(Enum):
    # Start/continue buying
    Start = 0
    # Stop buying
    End = 1
    # Sell all assets and stop
    Kill = 2

    def parse(ty: str) -> None | Self:
        match ty:
            case "start":
                return SymbolCommandTy.Start
            case "end":
                return SymbolCommandTy.End
            case "kill":
                return SymbolCommandTy.Kill

# Commands that act on stock symbols
class SymbolCommand(Command):
    exchange: str
    symbol: str
    ty: SymbolCommandTy

    def __init__(self, exchange: str, symbol: str, ty: SymbolCommandTy):
        self.symbol = symbol
        self.ty = ty

    async def execute(self, state: State):
        pass

    def parse(command: str) -> None | Self:
        match re.match(r"(\w+)/(\w+)@(\w+)", command):
            case re.Match() as matches:
                (ty, symbol, exchange) = matches.group(1, 2, 3)

                match SymbolCommandTy.parse(ty):
                    case SymbolCommandTy() as ty:
                        return SymbolCommand(exchange, symbol, ty)

COMMAND_PARSERS: list[Callable[str, None | Self]] = [
    SymbolCommand.parse
]
