# Limit Order Book Simulator

This is a modular simulation of a limit order book system, inspired by [Hudson River Trading's](https://github.com/hudson-trading/inside-at-hrt) public educational repository "inside-at-hrt". It aims to replicate core exchange mechanics such as order matching, price-time priority, and event-driven callbacks.

## Features

- Symbolic order tracking (supports multiple symbols like `AAPL`, `GOOG`, etc.)
- Full lifecycle: `add`, `update`, `cancel`, `exec` (with size control)
- Matching logic based on price-time priority
- Inside (top-of-book) change detection
- Rejection handling for invalid updates/cancels
- Modular architecture (`Book`, `MatchingEngine`, `Order`, `Side`)
- Extensible with event hooks for logging or GUI updates

## File Structure

| File                  | Description                                   |
|-----------------------|-----------------------------------------------|
| `main.py`             | Entry point for simulation                    |
| `side.py`             | Enum class for `Bid`, `Ask`, and `Invalid`    |
| `order.py`            | Order class with `symbol`, `side`, `price`, etc. |
| `book.py`             | Order book that manages internal state        |
| `matching_engine.py`  | Engine that matches and routes orders         |

## Example 

```python
from matching_engine import MatchingEngine
from order import Order
from side import Side

def on_inside(symbol, side):
    print(f"[INSIDE CHANGE] {symbol} {side.name}")

def on_reject(order):
    print(f"[REJECT] {order}")

engine = MatchingEngine()
engine.book.sub_on_inside(on_inside)
engine.sub_on_reject(on_reject)

engine.on_new(Order(\"AAPL\", Side.Bid, 100.0, 10))
engine.on_new(Order(\"AAPL\", Side.Ask, 99.0, 5))  # Executes with above
engine.on_update(Order(\"AAPL\", Side.Bid, 101.0, 20, refnum=999))  # Rejected
```


Installation
This project uses only standard Python libraries.

```bash
git clone https://github.com/your-username/limit-order-book-sim.git
cd limit-order-book-sim
python main.py
```
