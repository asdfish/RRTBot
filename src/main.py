import asyncio
import sys

from command import Command, COMMAND_PARSERS
from state import create_state, EnvVarError, State

async def main() -> int:
    match await create_state():
        case EnvVarError() as err:
            print(err)
            return 1
        case State() as state:
            while state.alive:
                line = (await asyncio.to_thread(sys.stdin.readline)).strip()

                match next(filter(lambda cmd:cmd is not None, map(lambda p:p(line), COMMAND_PARSERS)), None):
                    case None:
                        print(f"failed to parse command `{line}`")
                    case Command() as cmd:
                        await cmd.execute(state)

            return 0
        case _:
            return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
