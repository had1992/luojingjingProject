from window import *
from dataProcess import *
import Tkinter

if __name__ == '__main__':
    root = Tkinter.Tk()

    pW = printWrapper.PrintWrapper()
    dP = DataProcess(pW)
    w = Window(root, dP)

    root.mainloop()
    pass
