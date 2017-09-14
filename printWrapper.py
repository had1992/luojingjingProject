# coding=utf-8

import Tkinter

ERROR = 'ERROR'
WARN = 'WARN'
SUCCESS = 'SUCCESS'
NORMAL = 'NORMAL'

class PrintWrapper:
    def __init__(self):
        self.tC = None
        pass

    def setTextConsolo(self,textConsolo):
        self.tC = textConsolo

    def myPrint(self, infotype='', text=''):
        self.tC.insert(Tkinter.END, infotype+' '+text+'\n')

    def myPrintInfo(self, info):
        for key, value in info.items():
            if not key == 'text':
                self.tC.insert(Tkinter.END, key + ':' + value + '\n')
        self.tC.insert(Tkinter.END, info['text'] + '\n')
