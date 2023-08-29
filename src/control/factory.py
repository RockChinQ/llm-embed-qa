
import typing

T = typing.TypeVar("T")

__components__: dict[typing.Type, dict[str, typing.Type]] = {}


def component(base: typing.Type,name: str):
    """Decorator for registering a component."""

    def wrapper(cls: typing.Type):
        if base not in __components__:
            __components__[base] = {}
        __components__[base][name] = cls
        return cls

    return wrapper


def create(base: typing.Type[T], name: str, **kwargs) -> T:
    """Creates a component."""
    if base not in __components__:
        raise ValueError(f"{base} not registered.")
    if name not in __components__[base]:
        raise ValueError(f"{name} of {base} not registered.")
    return __components__[base][name](**kwargs)
