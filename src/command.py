from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable
import asyncio
import re

from ib_async import Stock

from state import State
from strategy import StrategyAction, strategy_action_parser

class Command(ABC):
    # TODO: create error sum type
    @abstractmethod
    async def execute(self, State) -> None:
        pass

# Commands that act on stock symbols
class SymbolCommand(Command):
    exchange: str
    symbol: str
    action: StrategyAction

    def __init__(self, exchange: str, symbol: str, action: StrategyAction) -> None:
        self.symbol = symbol
        self.action = action

    def to_stock(self) -> Stock:
        return Stock(symbol = self.symbol, exchange = self.exchange)

    async def execute(self, state: State) -> None:
        match (self.action, state.strategy_handlers.get(self.to_stock())):
            case (StrategyAction.Start, _):
                await state.start_stock(self.to_stock())
            case (action, (tx, _)):
                await tx.put(action)

def symbol_command_parser(command: str) -> None | Command:
    match re.match(r"(\w+)/(\w+)@(\w+)", command):
        case re.Match() as matches:
            (ty, symbol, exchange) = matches.group(1, 2, 3)

            match strategy_action_parser(ty):
                case str() as ty:
                    return SymbolCommand(exchange, symbol, ty)

    return None

def command_parsers() -> list[Callable[[str], None | Command]]:
    return [
        symbol_command_parser,
    ]
