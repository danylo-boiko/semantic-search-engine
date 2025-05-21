from dataclasses import dataclass

from sumy.models.dom import Sentence


@dataclass
class EvaluatedSentence:
    value: Sentence
    order: int
    rating: float
