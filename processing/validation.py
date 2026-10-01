def require_value(value, name: str):
    if value is None:
        raise ValueError(f"O valor '{name}' é obrigatório.")

    return value
