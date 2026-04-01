
from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.decision import decide_actions
from src.metrics import compute_summary, provider_breakdown


def main() -> None:
    root = Path(__file__).resolve().parent
    df = pd.read_csv(root / "data" / "sample_transactions.csv")
    results = decide_actions(df)
    summary = compute_summary(results)

    print("=== Payment Decision Engine Summary ===")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n=== Provider Breakdown ===")
    print(provider_breakdown(results).to_string(index=False))

    output_path = root / "data" / "results.csv"
    results.to_csv(output_path, index=False)
    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()
