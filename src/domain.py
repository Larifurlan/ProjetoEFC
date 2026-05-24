from dataclasses import dataclass
from enum import Enum
from typing import Callable, TypeAlias, TypedDict


class OrderItem(TypedDict):
    nome: str
    p: float
    q: int
    tipo: str


class OrderRecord(TypedDict):
    id: int
    cli: str
    itens: list[OrderItem]
    tot: float
    st: str
    dt: str
    tp: str


DbOrderRow: TypeAlias = tuple[int, str, str, float, str, str, str]
CalculateTotalClient: TypeAlias = Callable[[str], float]


@dataclass(frozen=True)
class OrderDraft:
    client_name: str
    items: list[OrderItem]
    total: float
    status: str
    date: str
    customer_type: str


class PaymentStatus(Enum):
    APPROVED = "aprovado"
    PENDING = "pendente"
    REJECTED = "rejeitado"
