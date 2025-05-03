import asyncio
import sys

from command import Command, COMMAND_PARSERS
from state import EnvVar, EnvVarError, State

async def main() -> int:
    match await State.new():
        case EnvVarError() as err:
            print(err)
            return 1
        case State() as state:
            while state.alive:
                line = (await asyncio.to_thread(sys.stdin.readline)).strip()

                for command_parser in COMMAND_PARSERS:
                    match command_parser(line):
                        case None:
                            print(f"failed to parse command `{line}`")
                        case Command() as command:
                            await command.execute(state)
            return 0
        case _:
            return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
