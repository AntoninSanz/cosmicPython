from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

def allocate(order_line, batches: List[Batch]):
    sorted_batches = sorted(batches, key=lambda x: (x.eta is not None, x.eta))
    for batch in sorted_batches:
        if batch.available_quantity >= order_line.qty:
            batch.available_quantity -= order_line.qty
            return batch
    return None
    
@dataclass(frozen=True)  #(1) (2)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):  #(2)
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine):  #(3)
        self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine):
        return self.available_quantity >= line.qty