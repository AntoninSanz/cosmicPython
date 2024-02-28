from datetime import date, timedelta
import pytest

from model import Batch, OrderLine, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
   batch = Batch("batch-002", "SMALL-TABLE", qty=20, eta=date.today())
   line = OrderLine("order-ref", "SMALL-TABLE", 2)

   assert batch.can_allocate(line)

def test_cannot_allocate_if_available_smaller_than_required():
   batch = Batch("batch-002", "SMALL-TABLE", qty=4, eta=date.today())
   line = OrderLine("order-ref", "SMALL-TABLE", 10)

   assert batch.can_allocate(line) is False


def test_can_allocate_if_available_equal_to_required():
   batch = Batch("batch-002", "SMALL-TABLE", qty=20, eta=date.today())
   line = OrderLine("order-ref", "SMALL-TABLE", 20)

   assert batch.can_allocate(line)


def test_prefers_warehouse_batches_to_shipments():
    in_warehouse_batch = Batch("warehouse-batch-001", "SMALL-TABLE", 100, eta=None)  
    shipment_batch = Batch("shipment-batch-001", "SMALL-TABLE", 100, eta=date.today())  
    order_line = OrderLine("order-123", "DECORATIVE-TRINKET", 10)

    allocate_batch = allocate(order_line, [in_warehouse_batch,shipment_batch])

    assert in_warehouse_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    batch = Batch("batch-002", "SMALL-TABLE", qty=20, eta=date.today())
    batch2 = Batch("batch-002", "SMALL-TABLE", qty=20, eta=date(2027, 12, 5))
    line = OrderLine("order-ref", "SMALL-TABLE", 5)

    allocate_batch = allocate(line, [batch,batch2])

    assert batch.available_quantity == 15
    assert batch2.available_quantity == 20
