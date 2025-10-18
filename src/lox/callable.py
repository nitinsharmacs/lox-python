from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from src.lox.env import Environment
from src.lox.stmt import FunDeclStmt

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


class LoxFunction(Callable):
    def __init__(self, funStmt: FunDeclStmt) -> None:
        self.funStmt = funStmt

    def call(self, interpreter: Interpreter, args: list[Any]) -> Any:
        env = Environment()

        for i, param in enumerate(self.funStmt.params):
            env.put(param.lexeme, args[i])

        interpreter.execute_block(self.funStmt.body, env)

    @property
    def arity(self) -> int:
        return len(self.funStmt.params)

    def __str__(self) -> str:
        return "<" + self.funStmt.name.lexeme + " fn>"
