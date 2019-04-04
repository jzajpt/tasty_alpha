import asyncio
from aiorun import run
import click
from .feed import FeedProcessor
from .backtest import run_backtest
from .feed import run_livefeed

@click.group()
def cli():
    pass

@click.command()
@click.option('--file', '-f', default='', help='Input CSV file')
@click.option('--bar-type', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
def backtest(file: str, bar_type: str, threshold: int) -> None:
    run(run_backtest(file, bar_type, threshold))

@click.command()
@click.option('--bar-type', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
def livefeed(bar_type: str, threshold: int) -> None:
    run_livefeed(bar_type, threshold)

cli.add_command(backtest)
cli.add_command(livefeed)

if __name__ == '__main__':
    cli()

