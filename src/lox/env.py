class Environment:
    def __init__(self):
        self.env = {}

    def get(self, key: str):
        return self.env[key]

    def put(self, key: str, value):
        self.env[key] = value

    def has(self, key: str) -> bool:
        try:
            self.env[key]
            return True
        except Exception as _:
            return False
