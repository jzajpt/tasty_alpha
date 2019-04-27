import asyncio
from aiorun import run
import click
import os
from .io.feed import run_livefeed
from .backtest.runner import run_backtest

@click.group()
def cli():
    pass


@click.command()
@click.option(
    '--strategy-file',
    '-f',
    required=True,
    type=click.Path(),
    help='Python file with your strategy'
)
@click.option(
    '--bar-type',
    '-b',
    default='tick',
    help='Bar type'
)
@click.option(
    '--threshold',
    '-t',
    type=int,
    default=None,
    help='Bar type'
)
def backtest(strategy_file, bar_type: str, threshold: int) -> None:
    run(run_backtest(strategy_file, bar_type, threshold))


@click.command()
@click.option(
    '--filename',
    '-f',
    required=True,
    type=click.Path(),
    help='Filename'
)
@click.option(
    '--library',
    '-l',
    required=True,
    type=str,
    help='Library to store the data'
)
@click.option(
    '--symbol',
    '-s',
    required=True,
    type=str,
    help='Symbol used to store/retrieve the data'
)
@click.option(
    '--source',
    type=str,
    help='Source of the data'
)
def ingest(filename: str,
           library: str,
           symbol: str,
           source: str) -> None:
    from .io.arctic import ingest_trades
    ingest_trades(filename, library, symbol)


@click.command()
@click.option(
    '--bar-type',
    '-b',
    default='tick',
    help='Bar type'
)
@click.option(
    '--threshold',
    '-t',
    type=int,
    default='',
    help='Bar type'
)
@click.option(
    '--pair',
    '-p',
    type=str,
    default='BTC-USDT',
    help='Pair'
)
def livefeed(bar_type: str, threshold: int, pair: str) -> None:
    run_livefeed(bar_type, threshold, pair)


cli.add_command(backtest)
cli.add_command(livefeed)
cli.add_command(ingest)

if __name__ == '__main__':
    cli()

