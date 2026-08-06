from dataclasses import dataclass


@dataclass
class HelloResponseDto:
    result: str
    square: int