import click
from .bar_generator import CSVTradeProcessor, DollarBars, TickBars

@click.command()
@click.option('--file', '-f', default='', help='Input CSV file')
def cli(file):
    bars = TickBars()
    trade_processor = CSVTradeProcessor(file)
    trade_processor.run()

if __name__ == '__main__':
    cli()

