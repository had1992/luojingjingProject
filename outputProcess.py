

#todo

class outputProcess:
    def __init__(self, outputFunc):
        self.of = outputFunc
        pass

    def myPrint(self, **info):
        self.outputFunc(info['text'])
