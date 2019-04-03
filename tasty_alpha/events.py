from aiopubsub import Key

NewBar = Key('new-bar')
NewTrade = Key('new-trade')

AnyNewBar = Key('*', 'new-bar')
AnyNewTrade = Key('*', 'new-trade')
AnyProcessingFinished = Key('*', 'new-trade')
