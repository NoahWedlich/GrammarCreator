from __future__ import annotations
from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Literal:
    value: str = ""

    def __str__(self) -> str:
        return self.value + " "

@dataclass(unsafe_hash=True)
class Lexeme:
    name: str = ""

    def __str__(self) -> str:
        return self.name + " "

@dataclass(unsafe_hash=True)
class LexemeList:
    body: tuple[Literal | Lexeme | LexemeList, ...]

    def __str__(self) -> str:
        result = "{"
        for l in self.body:
            result += str(l)
        result = result[:-1] + "}"
        return result

@dataclass(unsafe_hash=True)
class Rule:
    head: Lexeme
    body: tuple[Literal | Lexeme | LexemeList, ...]

    def __str__(self) -> str:
        result = f"{self.head}-> "
        for l in self.body:
            result += str(l)
        return result
