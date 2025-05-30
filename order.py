from side import Side

class Order:
    def __init__(self, symbol: str, side: Side, price: float, size: int, refnum: int = -1):
        self.symbol = symbol
        self.side = side
        self.price = price
        self.size = size
        self.refnum = refnum

    def __repr__(self):
        return f"Order({self.symbol}, {self.side.name}, P={self.price}, Q={self.size}, ID={self.refnum})"
