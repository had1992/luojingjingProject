# coding=utf-8

import ttk
import Tkinter
import tkFileDialog

class Window:
    """docstring for Window"""

    def __init__(self, master=None):
        self.master = master

        master.resizable(False, False)

        self.fileRoad = Tkinter.StringVar(master)
        self.dirRoad = Tkinter.StringVar(master)

        self.SNFileRoadLabel = Tkinter.Label(master, text='S/N文件路径：')
        self.SNFileRoadEntry = Tkinter.Entry(master, textvariable=self.fileRoad, width=60, state='readonly')
        self.chooseSNFileButton = Tkinter.Button(master, text='选择文件', command=self.chooseSNFile)

        self.dirRoadLabel = Tkinter.Label(master, text='目录路径：')
        self.dirRoadEntry = Tkinter.Entry(master, textvariable=self.dirRoad, width=60, state='readonly')
        self.chooseDirButton = Tkinter.Button(master, text='选择目录', command=self.chooseDir)

        self.readSNButton = Tkinter.Button(master, text='读取S/N')
        self.runButton = Tkinter.Button(master, text='开始工作')

        self.tvScrollBar = Tkinter.Scrollbar(master)
        self.treeview = ttk.Treeview(master, columns=('c1', 'c2', 'c3', 'c4', 'c5'), show="headings", height=20,
                                     yscrollcommand=self.tvScrollBar.set)
        self.tvScrollBar.configure(command=self.treeview.yview)
        self.treeview.heading('c1', text='S/N号')
        self.treeview.heading('c2', text='匹配文件数')
        self.treeview.heading('c3', text='最近测试日期')
        self.treeview.heading('c4', text='测试结果')
        self.treeview.heading('c5', text='测试文件')

        self.SNEntry = Tkinter.Entry(master)
        self.addSNButton = Tkinter.Button(master, text='手动添加S/N')
        self.deleteSNButton = Tkinter.Button(master, text='手动删除S/N')
        self.clearConsolsButton = Tkinter.Button(master, text='清除consolo')

        self.ctScrollBar = Tkinter.Scrollbar(master)
        self.consoloText = Tkinter.Text(master, height=20, width=142, yscrollcommand=self.ctScrollBar.set)
        self.ctScrollBar.configure(command=self.consoloText.yview)

        self.chooseDirButton['state'] = Tkinter.DISABLED
        self.readSNButton['state'] = Tkinter.DISABLED
        self.runButton['state'] = Tkinter.DISABLED

        self.__layout()

    def __layout(self):
        self.SNFileRoadLabel.grid(row=0, column=0, sticky='e')
        self.SNFileRoadEntry.grid(row=0, column=1, sticky='ew')
        self.chooseSNFileButton.grid(row=0, column=2)
        self.readSNButton.grid(row=0, column=3, sticky='w')

        self.dirRoadLabel.grid(row=1, column=0, sticky='e')
        self.dirRoadEntry.grid(row=1, column=1, sticky='ew')
        self.chooseDirButton.grid(row=1, column=2)
        self.runButton.grid(row=1, column=3, sticky='w')

        self.treeview.grid(row=3, column=0, columnspan=4)
        self.tvScrollBar.grid(row=3, column=4, sticky='ns')

        self.SNEntry.grid(row=4, column=0, sticky='we')
        self.addSNButton.grid(row=4, column=1, sticky='w')
        self.deleteSNButton.grid(row=4, column=2, sticky='w')
        self.clearConsolsButton.grid(row=4, column=3, sticky='e')

        self.consoloText.grid(row=5, column=0, columnspan=4)
        self.ctScrollBar.grid(row=5, column=4, sticky='ns')

    def chooseSNFile(self):
        fileName = tkFileDialog.askopenfilename(initialdir='.', filetypes=[('xls files', '*.xls'),
                                                                           ('xlsx files', '*.xlsx')])
        self.fileRoad.set(fileName)
        self.readSNButton['state'] = Tkinter.ACTIVE
        pass

    def chooseDir(self):
        dirName = tkFileDialog.askdirectory(initialdir='.')
        self.dirRoad.set(dirName)
        self.runButton['state'] = Tkinter.ACTIVE
        pass

