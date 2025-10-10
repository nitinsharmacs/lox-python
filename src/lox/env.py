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

    def put(self, key: str, value):
        self.env[key] = value

    def assign(self, key: str, value):
        if self.has(key):
            self.put(key, value)
            return

        if self.parent is not None:
            return self.parent.assign(key, value)

        raise ValueError("value not present")

    def has(self, key: str) -> bool:
        try:
            self.env[key]
            return True
        except Exception as _:
            return False
