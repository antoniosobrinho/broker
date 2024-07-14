from dataclasses import dataclass
from decimal import Decimal


@dataclass
class PerformanceDataClass:
    currency: str
    total_spend: Decimal
    money_gain_loss: Decimal
    current_money: Decimal
    pct: Decimal
