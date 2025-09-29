from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visitBinary(self, expr):
        pass

    @abstractmethod
    def visitUnary(self, expr):
        pass

    @abstractmethod
    def visitGrouping(self, expr):
        pass

    @abstractmethod
    def visitLiteral(self, expr):
        pass
