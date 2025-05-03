from enum import Enum
from functools import partial
from itertools import tee
from operator import itemgetter
from typing import Iterable, Self
import os

from ib_async import IB

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

ENV_VARS: list[EnvVar] = [
    EnvVar.Host,
    EnvVar.Port,
]

class EnvVarError:
    var: EnvVar

    def __init__(self, var: EnvVar) -> None:
        self.var = var

    def __str__(self) -> str:
        return f"environment variable `{self.var}` is missing"

class State:
    alive: bool = True
    ib: IB = IB()

    def __init__(self, ib: IB) -> None:
        self.ib = ib

async def create_state() -> EnvVarError | State:
    (env_vars, env_vars_filter) = tee(map(lambda v:(v, compose(EnvVar.__str__, os.environ.get)(v)), ENV_VARS))
    match next(map(compose(itemgetter(0), EnvVarError), filter(lambda v:v[1] is None, env_vars_filter)), None):
        case None:
            ib = IB()
            await partial(IB.connectAsync, ib, clientId = 1)(*map_snd(int, tuple(map(itemgetter(1), env_vars))))
            return State(ib)
        case EnvVarError() as err:
            return err
