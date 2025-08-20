import typer
from rich import print
from app.config import load_env
from app.brokers.alpaca_client import AlpacaClient
from app.exchanges.ccxt_client import CCXTClient

app = typer.Typer(help="Unified CLI for trading stocks (Alpaca) and crypto (ccxt)")

@app.command()
def account():
    """Show available accounts configured via .env"""
    cfg = load_env()
    if cfg.alpaca:
        print("[bold]Alpaca configured[/bold]")
    else:
        print("Alpaca not configured")
    if cfg.crypto:
        print(f"[bold]Crypto exchange configured:[/bold] {cfg.crypto.exchange}")
    else:
        print("Crypto exchange not configured")

@app.command()
def alpaca_info():
    """Show Alpaca account and positions"""
    cfg = load_env()
    assert cfg.alpaca, "Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env"
    client = AlpacaClient(cfg.alpaca)
    print(client.get_account())
    print(client.get_positions())

@app.command()
def alpaca_order(symbol: str, qty: float, side: str = typer.Option(..., help="buy or sell"), type_: str = "market"):
    cfg = load_env()
    assert cfg.alpaca, "Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env"
    client = AlpacaClient(cfg.alpaca)
    order = client.place_order(symbol=symbol, qty=qty, side=side, type_=type_)
    print(order)

@app.command()
def crypto_info():
    cfg = load_env()
    assert cfg.crypto, "Set CRYPTO_EXCHANGE, CRYPTO_API_KEY, CRYPTO_SECRET_KEY in .env"
    client = CCXTClient(cfg.crypto)
    print(client.fetch_balance())

@app.command()
def crypto_order(symbol: str, amount: float, side: str = typer.Option(..., help="buy or sell"), type_: str = "market", price: float = typer.Option(None)):
    cfg = load_env()
    assert cfg.crypto, "Set CRYPTO_EXCHANGE, CRYPTO_API_KEY, CRYPTO_SECRET_KEY in .env"
    client = CCXTClient(cfg.crypto)
    order = client.create_order(symbol=symbol, type_=type_, side=side, amount=amount, price=price)
    print(order)

if __name__ == "__main__":
    app()
