
from __future__ import annotations

import pandas as pd


PROVIDERS = {
    "acquirer_a": {"base_success": 0.96, "latency_ms": 540, "cost_pct": 0.015},
    "acquirer_b": {"base_success": 0.94, "latency_ms": 430, "cost_pct": 0.013},
    "acquirer_c": {"base_success": 0.91, "latency_ms": 320, "cost_pct": 0.010},
}


def choose_provider(row: pd.Series) -> str:
    """Simple routing logic balancing performance, cost, and risk."""
    method = row["payment_method"]
    risk_score = row["fraud_score"]
    amount = row["amount_eur"]
    country = row["country"]

    # Low-latency preference for transit-like small tickets
    if amount < 12 and method in {"contactless_card", "mobile_wallet", "wearable"}:
        return "acquirer_c"

    # Higher reliability for larger or riskier payments
    if risk_score >= 60 or amount >= 120:
        return "acquirer_a"

    # Cross-border payments prefer the balanced option
    if country not in {"FR", "LU", "BE", "NL", "DE", "ES", "IT"}:
        return "acquirer_b"

    return "acquirer_b"


def provider_expected_success(row: pd.Series) -> float:
    provider = row["selected_provider"]
    base = PROVIDERS[provider]["base_success"]

    # Penalize success under tougher scenarios
    penalty = 0.0
    if row["fraud_score"] >= 70:
        penalty += 0.10
    elif row["fraud_score"] >= 40:
        penalty += 0.05

    if row["previous_failures"] >= 2:
        penalty += 0.06
    elif row["previous_failures"] == 1:
        penalty += 0.03

    if row["is_cross_border"]:
        penalty += 0.02

    if row["payment_method"] == "card_not_present":
        penalty += 0.03

    return max(0.35, min(0.995, base - penalty))


def fallback_provider(primary: str) -> str:
    order = ["acquirer_a", "acquirer_b", "acquirer_c"]
    for p in order:
        if p != primary:
            return p
    return "acquirer_b"
