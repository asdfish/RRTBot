from asyncio import create_task, Queue, Task
from enum import Enum
from functools import partial
from itertools import tee
from operator import itemgetter
import os

from ib_async import IB, Stock, TickData

from strategy import StrategyAction, strategy_handler
from utils import compose, map_snd

class EnvVar(Enum):
    Host = 0
    Port = 1

    def __str__(self) -> str:
        match self:
            case EnvVar.Host:
                return "RRTBOT_IB_API_HOST"
            case EnvVar.Port:
                return "RRTBOT_IB_API_PORT"

class EnvVarError:
    var: EnvVar

    def __init__(self, var: EnvVar) -> None:
        self.var = var

    def __str__(self) -> str:
        return f"environment variable `{self.var}` is missing"

class State:
    alive: bool = True
    ib: IB
    # should only be used for transmission
    strategy_handlers: dict[Stock, tuple[Queue[StrategyAction], Task[None]]]

    def __init__(self, ib: IB) -> None:
        self.ib = ib

    # Start trading on this stock
    async def start_stock(self, stock: Stock) -> None:
        match self.strategy_handlers.get(stock, None):
            case (Queue(action_tx), Task()):
                await action_tx.put(StrategyAction.Start)
            case None:
                action_chan: Queue[StrategyAction] = Queue()

                self.strategy_handlers[stock] = (action_chan, create_task(strategy_handler(action_chan, self.ib.reqMktData(stock))))

async def create_state() -> EnvVarError | State:
    (env_vars, env_vars_filter) = tee(map(lambda v:(v, compose(EnvVar.__str__, os.environ.get)(v)), [EnvVar.Host, EnvVar.Port]))
    match next(map(compose(itemgetter(0), EnvVarError), filter(lambda v:v[1] is None, env_vars_filter)), None):
        case None:
            ib = IB()
            await partial(IB.connectAsync, ib, clientId = 1)(*map_snd(int, tuple(map(itemgetter(1), env_vars))))
            return State(ib)
        case EnvVarError() as err:
            return err
