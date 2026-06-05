def money_fmt(value):
    try:
        value = float(value)
    except Exception:
        return "$0"

    # Formato abreviado para cifras grandes (Estilo Latam)
    if abs(value) >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f} Billones"
    elif abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f} Mil Millones"
    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f} Millones"
    else:
        # Formato normal para valores menores a un millón
        formatted = f"{value:,.0f}"
        main_part = formatted.replace(",", ".")
        return f"${main_part}"


def int_fmt(value):
    try:
        return f"{int(float(value)):,}".replace(",", ".")
    except Exception:
        return "0"