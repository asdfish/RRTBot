from abc import ABC, abstractmethod
from asyncio import Queue, Task, create_task
from enum import Enum
from functools import partial
from operator import call, itemgetter
from typing import Callable, Generic
import asyncio

from ib_async import TickData, Ticker

from utils import compose, map_snd, filter_fst

class Decision(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class Buy(Decision):
    shares: float

    def __init__(self, shares: float) -> None:
        self.shares = shares

    def execute(self) -> None:
        # TODO
        pass

class Sell(Decision):
    shares: float

    def __init__(self, shares: float) -> None:
        self.shares = shares

    def execute(self) -> None:
        # TODO
        pass

# Decision that does nothing
class Null(Decision):
    def execute(self) -> None:
        pass

class Strategy(ABC):
    @abstractmethod
    def analyze(data: TickData) -> Decision:
        pass

def strategies() -> list[Strategy]:
    return []

class StrategyAction(Enum):
    Start = 0
    End = 1
    Kill = 2

def strategy_action_parser(action: str) -> None | StrategyAction:
    match action:
        case "start":
            return StrategyAction.Start
        case "end":
            return StrategyAction.End
        case "kill":
            return StrategyAction.Kill
        case _:
            return None

class StrategyPermission(Enum):
    Sell = 0
    All = 1

    def filter(self, decision: Decision) -> None | Decision:
        match self:
            case StrategyPermission.Sell:
                return decision if isinstance(decision, Sell) else None
            case StrategyPermission.All:
                return decision

class StrategyHandlerTasks:
    action_chan: Queue[StrategyAction]
    ticker_chan: Queue[TickData]
    tasks: list[Task] = []

    def __init__(self, action_chan: Queue[StrategyAction], ticker_chan: Queue[TickData]) -> None:
        self.action_chan = action_chan
        self.ticker_chan = ticker_chan
        self.replenish()

    def missing_task(self, task: str) -> bool:
        return next(filter(lambda t:t.get_name() == task, self.tasks), None) is None

    def replenish(self) -> None:
        self.tasks.extend(map(compose(itemgetter(1), call), filter(partial(filter_fst, self.missing_task), map(lambda t:(t[0], partial(t[1], name = t[0])), [
            ("action", partial(create_task, self.action_chan.get())),
            ("ticker", partial(create_task, self.ticker_chan.get())),
        ]))))

    async def recv(self) -> StrategyAction | TickData:
        done, pending = await asyncio.wait(self.tasks, return_when = asyncio.FIRST_COMPLETED)
        self.tasks = list(pending)
        self.replenish()

        return done.pop()

async def strategy_handler(action_chan: Queue[StrategyAction], ticker: Ticker) -> None:
    permission = StrategyPermission.All

    shares = 0.0
    strategies = strategies()

    ticker_chan: Queue[TickData] = Queue()
    ticker.updateEvent += lambda ticker:ticker_chan.put_nowait(ticker.ticks[len(ticker.ticks) - 1])

    tasks = StrategyHandlerTasks(action_chan, ticker_chan)

    while True:
        match await tasks.recv():
            case StrategyAction.Kill:
                Sell(shares).execute()
                return
            case StrategyAction.Start:
                permission = StrategyPermission.All
            case StrategyAction.End:
                permission = StrategyPermission.Sell
            case TickData() as data:
                for decision in map(compose(partial(Strategy.analyze, data = data), permission.filter), strategies):
                    match decision:
                        case Decision() as decision:
                            decision.execute()
