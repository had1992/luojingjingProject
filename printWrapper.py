

#todo

class PrintWrapper:
    def __init__(self, textConsolo):
        self.of = outputFunc
        pass

    def myPrint(self, **info):
        self.outputFunc(info['text'])
