import time
from typing import Any
from src.lox.callable import Callable
from src.lox.env import Environment


class Clock(Callable):
    def __init__(self) -> None:
        self.__arity = 0

    def call(self, interpreter, args: list[Any]) -> Any:
        return time.time()

    @property
    def arity(self):
        return self.__arity

    def __str__(self) -> str:
        return "<native fn>"


def set_natives(env: Environment):
    env.put("clock", Clock())


__all__ = ["set_natives"]
