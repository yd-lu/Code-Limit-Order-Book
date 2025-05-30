from matching_engine import MatchingEngine
from order import Order
from side import Side

def on_inside(symbol, side):
    print(f"[INSIDE CHANGE] {symbol} {side.name}")

def on_reject(order):
    print(f"[REJECT] {order}")

def main():
    engine = MatchingEngine()
    engine.book.sub_on_inside(on_inside)
    engine.sub_on_reject(on_reject)

    order1 = Order("AAPL", Side.Bid, 100.0, 10)
    order2 = Order("AAPL", Side.Ask, 99.0, 5)
    engine.on_new(order1)
    engine.on_new(order2)  # Should execute with order1

    bad_update = Order("AAPL", Side.Bid, 105.0, 20, refnum=999)
    engine.on_update(bad_update)  # Should reject

if __name__ == "__main__":
    main()
