
from __future__ import annotations

import numpy as np
import pandas as pd

from .fraud import compute_fraud_score, risk_band
from .routing import choose_provider, provider_expected_success, fallback_provider, PROVIDERS


def decide_actions(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    out = df.copy()

    out["fraud_score"] = compute_fraud_score(out)
    out["risk_band"] = out["fraud_score"].apply(risk_band)
    out["selected_provider"] = out.apply(choose_provider, axis=1)
    out["expected_success_rate"] = out.apply(provider_expected_success, axis=1).round(3)

    decisions = []
    fallback_used = []
    fallback_to = []
    final_status = []
    latency_ms = []
    gross_margin_eur = []

    for _, row in out.iterrows():
        provider = row["selected_provider"]
        provider_info = PROVIDERS[provider]
        expected_success = row["expected_success_rate"]

        if row["fraud_score"] >= 85:
            decision = "decline"
            used_fallback = False
            fb = None
            success = False
            latency = provider_info["latency_ms"]
        else:
            # High risk but not severe => manual review for higher amount flows
            if row["fraud_score"] >= 70 and row["amount_eur"] >= 80:
                decision = "review"
                used_fallback = False
                fb = None
                success = False
                latency = provider_info["latency_ms"]
            else:
                primary_success = rng.random() < expected_success
                if primary_success:
                    decision = "accept"
                    used_fallback = False
                    fb = None
                    success = True
                    latency = provider_info["latency_ms"]
                else:
                    if row["previous_failures"] <= 1 and row["fraud_score"] < 70:
                        fb = fallback_provider(provider)
                        fb_info = PROVIDERS[fb]
                        fb_success_rate = max(0.30, expected_success - 0.02 + 0.03)
                        fb_success = rng.random() < fb_success_rate
                        decision = "retry_fallback"
                        used_fallback = True
                        success = fb_success
                        latency = provider_info["latency_ms"] + fb_info["latency_ms"] + 120
                    else:
                        fb = None
                        used_fallback = False
                        success = False
                        decision = "decline"
                        latency = provider_info["latency_ms"]

        status = "approved" if success else ("review_required" if decision == "review" else "rejected")
        provider_fee = row["amount_eur"] * PROVIDERS[row["selected_provider"]]["cost_pct"]
        fallback_fee = row["amount_eur"] * PROVIDERS[fb]["cost_pct"] if fb else 0.0
        margin = row["amount_eur"] * 0.025 - provider_fee - fallback_fee

        decisions.append(decision)
        fallback_used.append(used_fallback)
        fallback_to.append(fb)
        final_status.append(status)
        latency_ms.append(int(latency))
        gross_margin_eur.append(round(margin, 2))

    out["decision"] = decisions
    out["fallback_used"] = fallback_used
    out["fallback_provider"] = fallback_to
    out["final_status"] = final_status
    out["simulated_latency_ms"] = latency_ms
    out["gross_margin_eur"] = gross_margin_eur
    return out
