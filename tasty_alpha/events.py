from aiopubsub import Key

NewBar = Key('new-bar')
NewTrade = Key('new-trade')
ProcessingFinished = Key('processing-finished')

AnyNewBar = Key('*', 'new-bar')
AnyNewTrade = Key('*', 'new-trade')
AnyProcessingFinished = Key('*', 'processing-finished')
