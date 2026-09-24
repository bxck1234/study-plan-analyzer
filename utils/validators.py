def validate_required(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{label}不能为空")
    return value


def validate_positive_int(value: int, label: str) -> int:
    if value <= 0:
        raise ValueError(f"{label}必须大于0")
    return value

