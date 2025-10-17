from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.lox.interpreter import Interpreter


class Callable(ABC):
    @abstractmethod
    def call(self, interpreter: Interpreter, args: list[Any]) -> Any:
        pass

    @property
    @abstractmethod
    def arity(self) -> int:
        pass
