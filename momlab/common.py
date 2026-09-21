"""Input validation, result files, and optional plots. Physics lives in each tier."""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inputs(case, positive=(), nonnegative=(), finite=()):
    """Return finite floats; reject missing, misspelled, and nonphysical inputs."""
    names = tuple(positive) + tuple(nonnegative) + tuple(finite)
    if set(case) != set(names):
        raise ValueError("Input keys differ: missing={}, unexpected={}".format(
            sorted(set(names) - set(case)), sorted(set(case) - set(names))))
    out = {}
    for name in names:
        raw = case[name]
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ValueError(name + " must be a number")
        value = float(raw)
        if not math.isfinite(value):
            raise ValueError(name + " must be finite")
        if name in positive and value <= 0:
            raise ValueError(name + " must be positive")
        if name in nonnegative and value < 0:
            raise ValueError(name + " must be nonnegative")
        out[name] = value
    return out


def linspace(start, stop, count=51):
    return [start + (stop - start) * i / (count - 1) for i in range(count)]


def capacity_ratio(capacity, demand):
    return capacity / abs(demand) if demand else "unbounded (zero demand)"


def table(name, rows, x, ys, xlabel, ylabel, log=False):
    return dict(name=name, rows=rows, x=x, ys=ys, xlabel=xlabel,
                ylabel=ylabel, log=log)


def result(title, metrics, tables, notes):
    return dict(title=title, metrics=metrics, tables=tables, notes=notes)


def plot_tables(tables, output):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ValueError("Plotting needs matplotlib: python3 -m pip install -r requirements-plot.txt") from exc
    for data in tables:
        fig, ax = plt.subplots(figsize=(7.6, 4.5), layout="constrained")
        for y in data["ys"]:
            ax.plot([r[data["x"]] for r in data["rows"]],
                    [r[y] for r in data["rows"]], label=y.replace("_", " "), linewidth=2)
        if data["log"]:
            ax.set_xscale("log")
            ax.set_yscale("log")
        ax.set(xlabel=data["xlabel"], ylabel=data["ylabel"],
               title=data["name"].replace("_", " ").title())
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8)
        fig.savefig(output / (data["name"] + ".png"), dpi=150)
        plt.close(fig)


def write_result(data, case, output, plot=False):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    payload = dict(inputs=case, **data)
    (output / "result.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    lines = ["# " + data["title"], "", "| Quantity | Value |", "|---|---:|"]
    for name, value in data["metrics"].items():
        formatted = "{:.9g}".format(value) if isinstance(value, (int, float)) else str(value)
        lines.append("| {} | {} |".format(name, formatted))
    lines.extend(["", "## Interpretation", ""] + ["- " + n for n in data["notes"]])
    lines.extend(["", "Inputs and full numerical tables are preserved in `result.json`.", ""])
    for data_table in data["tables"]:
        with (output / (data_table["name"] + ".csv")).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data_table["rows"][0]))
            writer.writeheader()
            writer.writerows(data_table["rows"])
    (output / "report.md").write_text("\n".join(lines))
    if plot:
        plot_tables(data["tables"], output)


def run_cli(solve, source):
    folder = Path(source).resolve().parent
    parser = argparse.ArgumentParser(description=solve.__doc__)
    parser.add_argument("--case", type=Path, default=folder / "cases" / "baseline.json")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / folder.name)
    parser.add_argument("--plot", action="store_true", help="also save PNG plots (requires matplotlib)")
    args = parser.parse_args()
    try:
        case = json.loads(args.case.read_text())
        data = solve(case)
        write_result(data, case, args.output, args.plot)
    except (ValueError, OSError, KeyError, TypeError, OverflowError) as exc:
        parser.exit(2, "Input/output error: {}\n".format(exc))
    print(data["title"])
    for name, value in data["metrics"].items():
        print("  {}: {}".format(name, "{:.8g}".format(value) if isinstance(value, (int, float)) else value))
    print("  Results: " + str(args.output.resolve()))
