from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from src.lox.env import Environment

if TYPE_CHECKING:
    from src.lox.expr import AnonymousFnExpr
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
    def __init__(
        self,
        fun: AnonymousFnExpr,
        closure: Environment,
        name: str | None = None,
    ) -> None:
        self.name = name
        self.funStmt = fun
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
        name = self.name if self.name is not None else "anonymous"
        return "<" + name + " fn>"
