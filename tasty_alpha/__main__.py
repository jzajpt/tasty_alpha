import click
from .bar_generator import CSVTradeProcessor, CSVBarWriter
from .bars import DollarBars, TickBars, VolumeBars
from .feed import FeedProcessor

@click.command()
@click.option('--file', '-f', default='', help='Input CSV file')
@click.option('--bar', '-b', default='tick', help='Bar type')
@click.option('--threshold', '-t', type=int, default='', help='Bar type')
def cli(file, bar, threshold):
    bars = None
    if bar == 'tick':
        bars = TickBars(threshold)
    elif bar == 'dollar':
        bars =  DollarBars(threshold)
    elif bar == 'volume':
        bars =  VolumeBars(threshold)
    else:
        print(f'Invalid bar: {bar}')
        return
    bar_writer = CSVBarWriter('output.csv')
    # trade_processor = CSVTradeProcessor(file)
    trade_processor = FeedProcessor()
    trade_processor.run()

@click.command()
def feed(file):
    print('feed')

if __name__ == '__main__':
    cli()

