
from __future__ import annotations

import pandas as pd


def compute_summary(df: pd.DataFrame) -> dict:
    total = len(df)
    approved = int((df["final_status"] == "approved").sum())
    rejected = int((df["final_status"] == "rejected").sum())
    review = int((df["final_status"] == "review_required").sum())
    fallback = int(df["fallback_used"].sum())

    return {
        "transactions": total,
        "approval_rate": round(approved / total * 100, 2) if total else 0.0,
        "rejection_rate": round(rejected / total * 100, 2) if total else 0.0,
        "review_rate": round(review / total * 100, 2) if total else 0.0,
        "fallback_rate": round(fallback / total * 100, 2) if total else 0.0,
        "avg_latency_ms": round(df["simulated_latency_ms"].mean(), 1) if total else 0.0,
        "avg_fraud_score": round(df["fraud_score"].mean(), 1) if total else 0.0,
        "gross_margin_total_eur": round(df["gross_margin_eur"].sum(), 2),
    }


def provider_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("selected_provider")
        .agg(
            transactions=("transaction_id", "count"),
            approval_rate=("final_status", lambda x: (x == "approved").mean() * 100),
            avg_latency_ms=("simulated_latency_ms", "mean"),
            avg_risk=("fraud_score", "mean"),
            gross_margin_eur=("gross_margin_eur", "sum"),
        )
        .reset_index()
    )
    return grouped.round(2)
