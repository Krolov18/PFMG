"""Measure parsing speed of a grammar over a file of sentences.

Usage:
    uv run python scripts/bench_parsing.py examples/data3 examples/phrases_data3.txt
    uv run python scripts/bench_parsing.py examples/data3 phrases.txt -n 5 10 -r 3
"""

import argparse
import statistics
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Literal

from pfmg.parsing.parser import KParser


def read_sentences(path: Path) -> list[str]:
    """Return the sentences of *path*, skipping blank and '#' lines.

    Args:
        path: Text file holding one sentence per line.

    Returns:
        list[str]: The sentences, in file order.

    """
    lines = path.read_text(encoding="utf8").splitlines()
    return [x.strip() for x in lines if x.strip() and not x.startswith("#")]


def measure(
    parser: KParser,
    sentences: list[str],
    keep: Literal["first", "all"],
    repeats: int,
) -> dict:
    """Parse *sentences* *repeats* times and return timings and result counts.

    Args:
        parser: The parser under test.
        sentences: Sentences to parse, one call per sentence.
        keep: "first" or "all".
        repeats: How many times to parse the whole batch.

    Returns:
        dict: Best and median batch duration, plus the number of translations.

    """
    durations: list[float] = []
    produced = 0
    for _ in range(repeats):
        start = time.perf_counter()
        results = (
            [parser.parse(data=x, keep="all") for x in sentences]
            if keep == "all"
            else [parser.parse(data=x, keep="first") for x in sentences]
        )
        durations.append(time.perf_counter() - start)
        produced = sum(len(x) if isinstance(x, list) else 1 for x in results)
    return {
        "best": min(durations),
        "median": statistics.median(durations),
        "produced": produced,
    }


def build_parser() -> argparse.ArgumentParser:
    """Return the command-line parser of this script."""
    cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    cli.add_argument("grammar", type=Path, help="grammar directory (five YAML files)")
    cli.add_argument("sentences", type=Path, help="text file, one sentence per line")
    cli.add_argument(
        "-n",
        "--sizes",
        type=int,
        nargs="+",
        default=(10, 20, 30, 40, 50),
        help="batch sizes to measure (default: 10 20 30 40 50)",
    )
    cli.add_argument(
        "-r", "--repeats", type=int, default=3, help="runs per batch (default: 3)"
    )
    cli.add_argument(
        "-k",
        "--keep",
        choices=("first", "all", "both"),
        default="both",
        help="parse mode to measure (default: both)",
    )
    return cli


def main(argv: Sequence[str] | None = None) -> int:
    """Run the benchmark and write a table to stdout.

    Args:
        argv: Command-line arguments; defaults to sys.argv[1:].

    Returns:
        int: Process exit code.

    """
    args = build_parser().parse_args(argv)
    sentences = read_sentences(args.sentences)

    too_big = [n for n in args.sizes if n > len(sentences)]
    if too_big:
        message = f"{args.sentences} n'a que {len(sentences)} phrases : {too_big} hors limite."
        raise SystemExit(message)

    lengths = [len(x.split()) for x in sentences]
    start = time.perf_counter()
    parser = KParser.from_yaml(args.grammar)
    build = time.perf_counter() - start

    try:
        parser.parse(data=sentences[0], keep="first")
    except ValueError as error:
        message = (
            f"{args.grammar} ne reconnaît pas la première phrase de "
            f"{args.sentences} : {error}"
        )
        raise SystemExit(message) from None

    out = sys.stdout.write
    out(
        f"{args.grammar} — {len(sentences)} phrases de {min(lengths)} à "
        f"{max(lengths)} mots (moyenne {statistics.mean(lengths):.1f})\n"
        f"construction du KParser : {build * 1000:.0f} ms\n"
        f"{args.repeats} passes par mesure, meilleur temps retenu\n\n"
    )
    header = f"{'keep':>6} {'phrases':>8} {'total':>10} {'par phrase':>12} {'phrases/s':>11} {'sorties':>9}\n"
    out(header)
    out("-" * (len(header) - 1) + "\n")

    modes: tuple[Literal["first", "all"], ...] = (
        ("first", "all") if args.keep == "both" else (args.keep,)
    )
    for keep in modes:
        for size in args.sizes:
            batch = sentences[:size]
            r = measure(parser, batch, keep, args.repeats)
            out(
                f"{keep:>6} {size:>8} {r['best'] * 1000:>8.1f} ms "
                f"{r['best'] / size * 1000:>9.2f} ms {size / r['best']:>11.0f} "
                f"{r['produced']:>9}\n"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
