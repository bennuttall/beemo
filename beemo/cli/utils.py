from typer import Exit, echo


def get_config():
    try:
        from beemo.settings import get_config

        return get_config()
    except Exception:
        return None


def require(value, name: str):
    if value is None:
        echo(f"Error: {name} must be set in config or provided as an option", err=True)
        raise Exit(1)
    return value
