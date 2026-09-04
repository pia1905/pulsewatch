def calculate_change_percent(
    last_seen_price: float,
    current_price: float
) -> float:
    if last_seen_price <= 0:
        return 0.0

    change = (
        (current_price - last_seen_price)
        / last_seen_price
    ) * 100

    return round(change, 2)


def calculate_attention_score(
    change_percent: float | None,
    volume_ratio: float | None = None,
    price_threshold: float = 3.0,
    volume_threshold: float = 1.5,
) -> int:
    """
    Personalized attention score.

    The score measures how strongly the current movement
    exceeds the user's own attention thresholds.
    """

    if change_percent is None:
        return 0

    price_threshold = max(price_threshold, 0.1)
    volume_threshold = max(volume_threshold, 1.0)

    absolute_change = abs(change_percent)

    # -------------------------
    # PRICE SIGNAL: 0 - 70
    # -------------------------

    price_multiple = (
        absolute_change / price_threshold
    )

    if price_multiple >= 3:
        price_score = 70
    elif price_multiple >= 2:
        price_score = 60
    elif price_multiple >= 1.5:
        price_score = 50
    elif price_multiple >= 1:
        price_score = 40
    elif price_multiple >= 0.5:
        price_score = 20
    else:
        price_score = 5

    # -------------------------
    # VOLUME SIGNAL: 0 - 30
    # -------------------------

    volume_score = 0

    if volume_ratio is not None:
        volume_multiple = (
            volume_ratio / volume_threshold
        )

        if volume_multiple >= 2:
            volume_score = 30
        elif volume_multiple >= 1.5:
            volume_score = 20
        elif volume_multiple >= 1:
            volume_score = 10

    return min(
        price_score + volume_score,
        100
    )


def classify_change(
    change_percent: float,
    volume_ratio: float | None = None,
    price_threshold: float = 3.0,
    volume_threshold: float = 1.5,
):
    absolute_change = abs(change_percent)

    price_triggered = (
        absolute_change >= price_threshold
    )

    volume_triggered = (
        volume_ratio is not None
        and volume_ratio >= volume_threshold
    )

    # HIGH:
    # Either personal price threshold or
    # unusual volume threshold is crossed.
    if price_triggered or volume_triggered:
        reasons = []

        if price_triggered:
            direction = (
                "up"
                if change_percent > 0
                else "down"
            )

            reasons.append(
                f"Price moved {absolute_change}% "
                f"{direction} since your last visit"
            )

        if volume_triggered:
            reasons.append(
                f"Volume is {round(volume_ratio, 2)}x "
                "the recent average"
            )

        return {
            "status": "HIGH",
            "reason": " • ".join(reasons),
        }

    # MEDIUM:
    # Half the user's price threshold.
    if absolute_change >= price_threshold / 2:
        direction = (
            "up"
            if change_percent > 0
            else "down"
        )

        return {
            "status": "MEDIUM",
            "reason": (
                f"Price moved {absolute_change}% "
                f"{direction} since your last visit"
            ),
        }

    return {
        "status": "STABLE",
        "reason": (
            "Movement is below your "
            "attention threshold"
        ),
    }


def analyze_stock(
    last_seen_price: float,
    current_price: float,
    volume_ratio: float | None = None,
    price_threshold: float = 3.0,
    volume_threshold: float = 1.5,
):
    change_percent = calculate_change_percent(
        last_seen_price,
        current_price
    )

    classification = classify_change(
        change_percent=change_percent,
        volume_ratio=volume_ratio,
        price_threshold=price_threshold,
        volume_threshold=volume_threshold,
    )

    attention_score = calculate_attention_score(
        change_percent=change_percent,
        volume_ratio=volume_ratio,
        price_threshold=price_threshold,
        volume_threshold=volume_threshold,
    )

    return {
        "change_percent": change_percent,
        "volume_ratio": volume_ratio,
        "status": classification["status"],
        "reason": classification["reason"],
        "attention_score": attention_score,
        "price_multiple": round(
            abs(change_percent) / max(price_threshold, 0.1),
            2
        ),
    }