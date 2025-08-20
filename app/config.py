from pydantic import BaseModel, Field
from typing import Optional
import os

class AlpacaConfig(BaseModel):
    api_key: str = Field(..., description="Alpaca API Key")
    secret_key: str = Field(..., description="Alpaca Secret Key")
    paper: bool = Field(True, description="Use paper trading")

class CryptoExchangeConfig(BaseModel):
    exchange: str = Field(..., description="Exchange id for ccxt, e.g. 'binance' or 'coinbasepro'")
    api_key: str
    secret_key: str
    password: Optional[str] = None

class AppConfig(BaseModel):
    alpaca: Optional[AlpacaConfig] = None
    crypto: Optional[CryptoExchangeConfig] = None


def load_env() -> AppConfig:
    from dotenv import load_dotenv
    load_dotenv()

    alpaca = None
    if os.getenv("ALPACA_API_KEY") and os.getenv("ALPACA_SECRET_KEY"):
        alpaca = AlpacaConfig(
            api_key=os.getenv("ALPACA_API_KEY"),
            secret_key=os.getenv("ALPACA_SECRET_KEY"),
            paper=os.getenv("ALPACA_PAPER", "true").lower() in ("1", "true", "yes")
        )

    crypto = None
    if os.getenv("CRYPTO_EXCHANGE") and os.getenv("CRYPTO_API_KEY") and os.getenv("CRYPTO_SECRET_KEY"):
        crypto = CryptoExchangeConfig(
            exchange=os.getenv("CRYPTO_EXCHANGE"),
            api_key=os.getenv("CRYPTO_API_KEY"),
            secret_key=os.getenv("CRYPTO_SECRET_KEY"),
            password=os.getenv("CRYPTO_PASSWORD")
        )

    return AppConfig(alpaca=alpaca, crypto=crypto)
