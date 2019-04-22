from .io.arctic import ingest_trades

def run_ingest(filename: str, name: str) -> None:
    ingest_trades(filename, name)
