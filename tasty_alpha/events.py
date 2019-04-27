from aiopubsub import Key

ProcessingFinished = Key('processing-finished')

AnyNewBar = Key('*', '*', 'new-bar')
AnyNewTrade = Key('*', '*', 'new-trade')
AnyProcessingFinished = Key('*', 'processing-finished')
