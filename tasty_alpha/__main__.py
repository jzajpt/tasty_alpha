import asyncio
from aiorun import run
import click
from .feed import FeedProcessor
from .backtest import run_backtest

@click.group()
def cli():
    pass

@click.command()
@click.option('--file', '-f', default='', help='Input CSV file')
@click.option('--bar', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
def backtest(file: str, bar: str, threshold: int) -> None:
    run(run_backtest(file, bar, threshold))

@click.command()
@click.option('--bar', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
def livefeed(bar: str, threshold: int) -> None:
    bars = new_bars(bar, threshold)
    trade_processor = FeedProcessor()
    trade_processor.run()


cli.add_command(backtest)
cli.add_command(livefeed)

if __name__ == '__main__':
    cli()

