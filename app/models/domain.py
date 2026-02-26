from dataclasses import dataclass


@dataclass
class CustomerFeatures:
    customer_id: int
    features: dict


@dataclass
class Recommendation:
    items: list


@dataclass
class RiskAssessment:
    score: float
