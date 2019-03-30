import click
from .csv_io import CSVTradeProcessor, CSVBarWriter
from .bars import DollarBars, TickBars, VolumeBars
from .feed import FeedProcessor

def new_bars(bar, threshold):
    if bar == 'tick':
        return TickBars(threshold)
    elif bar == 'dollar':
        return  DollarBars(threshold)
    elif bar == 'volume':
        return  VolumeBars(threshold)
    else:
        raise Exception(f'Invalid bar: {bar}')


@click.group()
def cli():
    pass

@click.command()
@click.option('--file', '-f', default='', help='Input CSV file')
@click.option('--bar', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
def backtest(file, bar, threshold):
    bars = new_bars(bar, threshold)
    bar_writer = CSVBarWriter('output.csv')
    trade_processor = CSVTradeProcessor(file)
    trade_processor.run()

@click.command()
@click.option('--bar', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
def livefeed(bar, threshold):
    bars = new_bars(bar, threshold)
    trade_processor = FeedProcessor()
    trade_processor.run()


cli.add_command(backtest)
cli.add_command(livefeed)

if __name__ == '__main__':
    cli()

