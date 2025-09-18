from typing import Optional, Dict, Any
import ccxt
from app.config import CryptoExchangeConfig

class CCXTClient:
    def __init__(self, cfg: CryptoExchangeConfig):
        if not hasattr(ccxt, cfg.exchange):
            raise ValueError(f"Exchange {cfg.exchange} not supported by ccxt")
        klass = getattr(ccxt, cfg.exchange)
        params = {
            'apiKey': cfg.api_key,
            'secret': cfg.secret_key,
        }
        if cfg.password:
            params['password'] = cfg.password
        self.exchange = klass(params)

    def get_markets(self):
        return self.exchange.load_markets()

    def fetch_balance(self):
        return self.exchange.fetch_balance()

    def create_order(self, symbol: str, type_: str, side: str, amount: float, price: Optional[float] = None, params: Optional[Dict[str, Any]] = None):
        return self.exchange.create_order(symbol, type_, side, amount, price, params or {})

    def cancel_order(self, id: str, symbol: Optional[str] = None):
        return self.exchange.cancel_order(id, symbol)

    def fetch_open_orders(self, symbol: Optional[str] = None):
        return self.exchange.fetch_open_orders(symbol)

