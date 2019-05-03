import asyncio
from aiorun import run
import click
from click_datetime import Datetime
from datetime import datetime
import os
from .live.runner import run_livefeed
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
    '-s',
    '--start',
    type=Datetime('%Y-%m-%d'),
    help='The start date of the backtest.',
)
@click.option(
    '-e',
    '--end',
    type=Datetime('%Y-%m-%d'),
    default=datetime.now(),
    help='The end date of the backtest.',
)
@click.option(
    '--bar-type',
    '-b',
    type=click.Choice(['tick', 'volume', 'dollar', 'tib']),
    default='tick',
    help='Bar type for backtest'
)
@click.option(
    '--threshold',
    '-t',
    type=int,
    default=None,
    help='Threshold value'
)
def backtest(strategy_file: str,
             start: Datetime,
             end: Datetime,
             bar_type: str,
             threshold: int) -> None:
    run(run_backtest(strategy_file, start, end, bar_type, threshold))


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
    '--strategy-file',
    '-f',
    required=True,
    type=click.Path(),
    help='Python file with your strategy'
)
@click.option(
    '--bar-type',
    '-b',
    type=click.Choice(['tick', 'volume', 'dollar', 'tib']),
    default='tick',
    help='Bar type'
)
@click.option(
    '--threshold',
    '-t',
    type=int,
    default='',
    help='Threshold value'
)
@click.option(
    '--exchange',
    '-e',
    type=click.Choice(['Binance', 'Bitfinex', 'Bitstamp', 'Coinbase', 'Kraken']),
    default='Binance',
    help='Exchange'
)
@click.option(
    '--pair',
    '-p',
    type=str,
    default='BTC-USDT',
    help='Pair'
)
def livefeed(strategy_file: str,
             bar_type: str,
             threshold: int,
             exchange: str,
             pair: str) -> None:
    run_livefeed(strategy_file, bar_type, threshold, exchange, pair)


cli.add_command(backtest)
cli.add_command(livefeed)
cli.add_command(ingest)

if __name__ == '__main__':
    cli()

