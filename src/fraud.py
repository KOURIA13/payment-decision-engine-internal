
from __future__ import annotations

import numpy as np
import pandas as pd


def compute_fraud_score(df: pd.DataFrame) -> pd.Series:
    """Return a simple fraud/risk score between 0 and 100.

    The model is intentionally transparent:
    - higher basket amounts increase risk
    - repeated retries increase risk
    - cross-border and late-night transactions increase risk
    - new users are slightly riskier
    - wallet/card-not-present flows are slightly riskier than chip/contactless
    """
    amount_component = np.clip(df["amount_eur"] / 8.0, 0, 35)
    retry_component = np.clip(df["previous_failures"] * 10, 0, 20)
    cross_border_component = df["is_cross_border"].astype(int) * 12
    late_night_component = df["hour"].isin([0, 1, 2, 3, 4, 5]).astype(int) * 10
    new_user_component = (~df["is_returning_user"]).astype(int) * 8
    channel_component = df["payment_method"].map({
        "contactless_card": 2,
        "mobile_wallet": 5,
        "wearable": 4,
        "card_not_present": 9,
    }).fillna(3)

    raw_score = (
        amount_component
        + retry_component
        + cross_border_component
        + late_night_component
        + new_user_component
        + channel_component
    )
    return pd.Series(np.clip(raw_score, 0, 100), index=df.index).round(1)


def risk_band(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
