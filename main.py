#!/usr/bin/env python3
"""One Line, No Deadline Met — make.fun bounty entry.

Writes a single-line joke (at most 200 characters) giving an excuse
for a missed deadline to /output/entry.txt (plus $ENTRY_OUT, whether
it names a file or a directory, and $ENTRY_OUT_DIR), and prints the
line to stdout exactly once. Standard library only.
"""

import os
import sys

# The excuse itself: one sentence, first person, the punch lands on
# the last words — an optimistic estimate measured in developer days,
# which turn out to run on dog years.
DEADLINE_LINE = (
    "I missed the deadline because I estimated the job in developer "
    "days, and developer days are measured in dog years."
)

STANDARD_ENTRY_PATH = "/output/entry.txt"


def check_length(line: str) -> None:
    """Raise unless the line fits the gate: 1 to 200 characters."""
    if not 0 < len(line) <= 200:
        raise ValueError(
            f"entry is {len(line)} characters, must be 1-200"
        )


def compose_line() -> str:
    """Return the entry line after enforcing the bounty character cap."""
    check_length(DEADLINE_LINE)
    return DEADLINE_LINE


def entry_out_target() -> str | None:
    """Translate $ENTRY_OUT into an entry.txt path, or None if unset."""
    entry_out = os.environ.get("ENTRY_OUT")
    if not entry_out:
        return None
    if os.path.isdir(entry_out):
        return os.path.join(entry_out, "entry.txt")
    return entry_out


def collect_targets() -> list:
    """Return every entry.txt path the line must be written to."""
    targets = [STANDARD_ENTRY_PATH]
    extra = entry_out_target()
    if extra:
        targets.append(extra)
    entry_out_dir = os.environ.get("ENTRY_OUT_DIR")
    if entry_out_dir:
        targets.append(os.path.join(entry_out_dir, "entry.txt"))
    return targets


def save_entry(line: str, path: str) -> None:
    """Write the entry line to path, creating parent dirs as needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)


def main() -> int:
    line = compose_line()
    print(line)
    sys.stdout.flush()
    for target in collect_targets():
        save_entry(line, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
