from book import Book
from order import Order
from side import Side
from typing import Callable

class MatchingEngine:
    def __init__(self):
        self.book = Book()
        self.subscribed_books = []
        self.reject_callbacks = []
        self.ref_counter = 1

    def on_new(self, order: Order) -> int:
        order.refnum = self.ref_counter
        self.ref_counter += 1

        opposite = Side.Bid if order.side == Side.Ask else Side.Ask
        while True:
            best = self.book._get_best(order.symbol, opposite)
            if not best:
                break
            top = best[0]
            if (order.side == Side.Ask and top.price < order.price) or \
               (order.side == Side.Bid and top.price > order.price):
                break
            fill = min(order.size, top.size)
            exec_order = Order(order.symbol, opposite, top.price, fill, top.refnum)
            self.book.on_exec(exec_order)
            self._call_exec(exec_order)
            order.size -= fill
            if order.size == 0:
                return order.refnum

        self.book.on_add(order)
        self._call_add(order)
        return order.refnum

    def on_update(self, order: Order):
        try:
            self.book.on_update(order)
            self._call_update(order)
        except ValueError:
            self._call_reject(order)

    def on_cancel(self, order: Order):
        try:
            self.book.on_cancel(order)
            self._call_cancel(order)
        except ValueError:
            self._call_reject(order)

    def subscribe_book(self, book: Book):
        self.subscribed_books.append(book)

    def sub_on_reject(self, cb: Callable[[Order], None]):
        self.reject_callbacks.append(cb)

    def _call_add(self, order: Order):
        for book in self.subscribed_books:
            book.on_add(order)

    def _call_update(self, order: Order):
        for book in self.subscribed_books:
            book.on_update(order)

    def _call_cancel(self, order: Order):
        for book in self.subscribed_books:
            book.on_cancel(order)

    def _call_exec(self, order: Order):
        for book in self.subscribed_books:
            book.on_exec(order)

    def _call_reject(self, order: Order):
        for cb in self.reject_callbacks:
            cb(order)
