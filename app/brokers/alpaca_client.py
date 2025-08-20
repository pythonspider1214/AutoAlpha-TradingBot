from typing import Optional
from alpaca_trade_api.rest import REST, TimeFrame
from app.config import AlpacaConfig

class AlpacaClient:
    def __init__(self, cfg: AlpacaConfig):
        base_url = 'https://paper-api.alpaca.markets' if cfg.paper else 'https://api.alpaca.markets'
        self.client = REST(key_id=cfg.api_key, secret_key=cfg.secret_key, base_url=base_url, api_version='v2')

    def get_account(self):
        return self.client.get_account()._raw

    def get_positions(self):
        return [p._raw for p in self.client.list_positions()]

    def place_order(self, symbol: str, qty: float, side: str, type_: str = 'market', time_in_force: str = 'day', limit_price: Optional[float] = None, stop_price: Optional[float] = None):
        order = self.client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type_,
            time_in_force=time_in_force,
            limit_price=limit_price,
            stop_price=stop_price
        )
        return order._raw

    def cancel_order(self, order_id: str):
        self.client.cancel_order(order_id)
        return {"status":"canceled","order_id":order_id}

    def list_orders(self, status: str = 'open'):
        return [o._raw for o in self.client.list_orders(status=status)]

