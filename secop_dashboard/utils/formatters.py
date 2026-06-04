def money_fmt(value):
    try:
        value = float(value)
    except Exception:
        return "$0"

    formatted = f"{value:,.2f}"

    main_part, decimal_part = formatted.split(".")
    main_part = main_part.replace(",", ".")

    return f"${main_part},{decimal_part}"


def int_fmt(value):
    try:
        return f"{int(float(value)):,}".replace(",", ".")
    except Exception:
        return "0"