from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from src.lox.env import Environment
from src.lox.stmt import FunDeclStmt

if TYPE_CHECKING:
    from src.lox.interpreter import Interpreter


class Return(Exception):
    def __init__(self, value, *args: object) -> None:
        self.value = value
        super().__init__(*args)


class Callable(ABC):
    @abstractmethod
    def call(self, interpreter: Interpreter, args: list[Any]) -> Any:
        pass

    @property
    @abstractmethod
    def arity(self) -> int:
        pass


class LoxFunction(Callable):
    def __init__(self, funStmt: FunDeclStmt, closure: Environment) -> None:
        self.funStmt = funStmt
        self.closure = closure

    def call(self, interpreter: Interpreter, args: list[Any]) -> Any:
        env = Environment(self.closure)

        for i, param in enumerate(self.funStmt.params):
            env.put(param.lexeme, args[i])

        try:
            interpreter.execute_block(self.funStmt.body, env)
        except Return as ret:
            return ret.value

    @property
    def arity(self) -> int:
        return len(self.funStmt.params)

    def __str__(self) -> str:
        return "<" + self.funStmt.name.lexeme + " fn>"
