from collections import defaultdict
from typing import Callable
from order import Order
from side import Side

class Book:
    def __init__(self):
        self.book = defaultdict(lambda: defaultdict(list))  # book[side][symbol] -> list[Order]
        self._cbs = []

    def sub_on_inside(self, cb: Callable[[str, Side], None]):
        self._cbs.append(cb)

    def _fire_inside_change(self, symbol: str, side: Side):
        for cb in self._cbs:
            cb(symbol, side)

    def on_add(self, order: Order) -> int:
        old = self._get_best(order.symbol, order.side)
        self.book[order.side][order.symbol].append(order)
        new = self._get_best(order.symbol, order.side)
        if old != new:
            self._fire_inside_change(order.symbol, order.side)
        return order.refnum

    def on_update(self, order: Order):
        bucket = self.book[order.side][order.symbol]
        old = self._get_best(order.symbol, order.side)
        for existing in bucket:
            if existing.refnum == order.refnum:
                existing.price = order.price
                existing.size = order.size
                new = self._get_best(order.symbol, order.side)
                if old != new:
                    self._fire_inside_change(order.symbol, order.side)
                return
        raise ValueError(f"Order {order.refnum} not found for update")

    def on_cancel(self, order: Order):
        for side in [Side.Bid, Side.Ask]:
            bucket = self.book[side][order.symbol]
            old = self._get_best(order.symbol, side)
            for existing in bucket:
                if existing.refnum == order.refnum:
                    if order.size == 0 or order.size == existing.size:
                        bucket.remove(existing)
                    elif order.size < existing.size:
                        existing.size -= order.size
                    else:
                        raise ValueError("Cancel size exceeds resting order size")
                    new = self._get_best(order.symbol, side)
                    if old != new:
                        self._fire_inside_change(order.symbol, side)
                    return
        raise ValueError(f"Order {order.refnum} not found for cancel")

    def on_exec(self, order: Order):
        for side in [Side.Bid, Side.Ask]:
            bucket = self.book[side][order.symbol]
            old = self._get_best(order.symbol, side)
            for existing in list(bucket):
                if existing.refnum == order.refnum:
                    if order.size == 0 or existing.size == order.size:
                        bucket.remove(existing)
                    elif order.size < existing.size:
                        existing.size -= order.size
                    else:
                        raise ValueError("Exec size too large")
                    new = self._get_best(order.symbol, side)
                    if old != new:
                        self._fire_inside_change(order.symbol, side)
                    return
        raise ValueError(f"Order {order.refnum} not found for exec")

    def _get_best(self, symbol: str, side: Side) -> list[Order]:
        bucket = self.book[side][symbol]
        if not bucket:
            return []
        if side == Side.Bid:
            best_price = max(o.price for o in bucket)
        else:
            best_price = min(o.price for o in bucket)
        return [o for o in bucket if o.price == best_price]
