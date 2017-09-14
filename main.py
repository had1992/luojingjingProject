from window import *
from dataProcess import *
import Tkinter

if __name__ == '__main__':
    root = Tkinter.Tk()
    dP = DataProcess()
    w = Window(root, dP)
    root.mainloop()
    pass
