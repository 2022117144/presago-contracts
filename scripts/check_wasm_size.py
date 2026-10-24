"""Enforce the release WASM byte budget used by CI (standard library only)."""

import argparse
from pathlib import Path
import sys

# Initial project ceiling, not a claim about a particular network's limits.
# Update only alongside a measured release artifact and a reviewed rationale.
BUDGET_BYTES = 128 * 1024
DEFAULT_ARTIFACT = Path("target/wasm32v1-none/release/prediction_market.wasm")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", nargs="?", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args(argv)
    try:
        if not args.artifact.is_file():
            raise OSError("expected a regular WASM artifact")
        size = args.artifact.stat().st_size
    except OSError as error:
        print(f"WASM size check failed: {args.artifact}: {error}", file=sys.stderr)
        return 1
    print(f"{args.artifact}: {size} bytes / {BUDGET_BYTES} byte budget")
    if size == 0:
        print("WASM size check failed: artifact is empty", file=sys.stderr)
        return 1
    if size > BUDGET_BYTES:
        print(f"WASM size check failed: exceeds budget by {size - BUDGET_BYTES} bytes", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
