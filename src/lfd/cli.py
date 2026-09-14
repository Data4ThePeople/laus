"""Command line entry: `lfd ingest`, `lfd classify`. Stages C to E are added
as they are built (`lfd snapshot t0 t1`, `lfd viz`)."""

from __future__ import annotations

import sys

from lfd import classify, compare, ingest

COMMANDS = {
    "ingest": ingest.main,
    "classify": classify.main,
    "snapshot": compare.main,
}


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: lfd {{{','.join(COMMANDS)}}} [options]")
        sys.exit(2)
    COMMANDS[argv[0]](argv[1:])


if __name__ == "__main__":
    main()
