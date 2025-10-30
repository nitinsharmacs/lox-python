from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from src.lox.env import Environment

if TYPE_CHECKING:
    from src.lox.token import Token
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


class LoxClass(Callable):
    def __init__(self, name: Token, methods: dict[str, LoxFunction]):
        self.__name = name
        self.__methods = methods

    def call(self, interpreter: Interpreter, args: list[Any]) -> Any:
        return LoxInstance(self)

    def get_method(self, name: str) -> LoxFunction | None:
        return self.__methods.get(name)

    @property
    def name(self) -> str:
        return self.__name.lexeme

    @property
    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<class " + self.name + ">"


class LoxInstance:
    def __init__(self, klass: LoxClass) -> None:
        self.klass = klass
        self.fields: dict[str, Any] = {}

    def get(self, property_name: str):
        if self.fields.get(property_name) is not None:
            return self.fields[property_name]

        method = self.klass.get_method(property_name)
        if method is not None:
            return method

        raise ValueError("Undefined property")

    def set(self, property_name: str, value):
        self.fields[property_name] = value

    def __str__(self) -> str:
        return "<instance of " + self.klass.name + ">"
