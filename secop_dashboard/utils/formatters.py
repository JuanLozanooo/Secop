def money_fmt(value):
    try:
        value = float(value)
    except Exception:
        return "$0"
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f} B"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f} M"
    if abs(value) >= 1_000:
        return f"${value/1_000:.2f} K"
    return f"${value:,.0f}"


def int_fmt(value):
    try:
        return f"{int(float(value)):,}".replace(",", ".")
    except Exception:
        return "0"
