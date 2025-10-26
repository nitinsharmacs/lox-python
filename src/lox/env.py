from __future__ import annotations


class Environment:
    def __init__(self, parent: Environment | None = None):
        self.env = {}
        self.parent = parent

    def get(self, key: str):
        if self.has(key):
            return self.env[key]

        if self.parent is not None:
            return self.parent.get(key)

        raise ValueError("value not present")

    def get_at(self, pos: int, key: str):
        env = self.ancester(pos)

        if env is not None:
            return env.get(key)

        return self.get(key)

    def ancester(self, pos: int) -> Environment | None:
        env = self

        for i in range(pos):
            env = self.parent

        return env

    def put(self, key: str, value):
        self.env[key] = value

    def assign(self, key: str, value):
        if self.has(key):
            self.put(key, value)
            return

        if self.parent is not None:
            return self.parent.assign(key, value)

        raise ValueError("value not present")

    def assign_at(self, pos: int, key: str, value):
        env = self.ancester(pos)

        if env is not None:
            return env.assign(key, value)

        self.assign(key, value)

    def has(self, key: str) -> bool:
        try:
            self.env[key]
            return True
        except Exception as _:
            return False
