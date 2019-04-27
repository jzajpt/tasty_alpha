import asyncio
from aiorun import run
import click
import os
from .io.feed import run_livefeed
from .backtest.runner import run_backtest, run_backtest_from_file

@click.group()
def cli():
    pass


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
    default=None,
    help='Bar type'
)
def backtest(file: str, bar_type: str, threshold: int) -> None:
    run(run_backtest(bar_type, threshold))


@click.command()
@click.option(
    '--filename',
    '-f',
    type=click.Path(),
    help='Filename'
)
@click.option(
    '--library',
    '-l',
    type=str,
    help='Library to store the data'
)
@click.option(
    '--symbol',
    '-s',
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
@click.option('--bar-type', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
@click.option('--pair', '-p', type=str, default='BTC-USDT', help='Bar type')
def livefeed(bar_type: str, threshold: int, pair: str) -> None:
    run_livefeed(bar_type, threshold, pair)


cli.add_command(backtest)
cli.add_command(livefeed)
cli.add_command(ingest)

if __name__ == '__main__':
    cli()

