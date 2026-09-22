from __future__ import annotations

import sys

from aether.kernel import Aether


def main() -> None:
    os_ = Aether()
    print("Aether OS  — type help.  ctrl-d to leave.")
    print(os_.reply("who"))
    while True:
        try:
            line = input("you> ")
        except (EOFError, KeyboardInterrupt):
            print("\nAether sleeping. Linux remains.")
            return
        out = os_.reply(line)
        if out:
            print(out)


if __name__ == "__main__":
    main()
