import asyncio
import os
import sys

from command import Command, COMMAND_PARSERS
from state import State

async def main() -> int:
    match os.environ.get("RRTBOT_IB_GATEWAY_SOCKET", None):
        case None:
            print("environment variable `RRTBOT_IB_GATEWAY_SOCKET` is not set")
            return 1
        case str() as socket:
            state = State(socket)

            while state.alive:
                line = (await asyncio.to_thread(sys.stdin.readline)).strip()

                for command_parser in COMMAND_PARSERS:
                    match command_parser(line):
                        case None:
                            print(f"failed to parse command `{line}`")
                        case Command() as command:
                            await command.execute(state)

            return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
