from abc import ABC


class DukanBaseException(ABC, Exception):
    def __init__(self, msg: str):
        if msg:
            self.msg = msg
