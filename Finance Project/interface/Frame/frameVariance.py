import tkinter as tk
from interface.App import App

class FrameVariance(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.parent=master

        tk.Label(self, text="Variance").pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Return to the menu", command=lambda: [self.canvas.destroy(), vbar.destroy(), hbar.destroy(), master.switch_frame(StartPage)]).pack()

        self.canvas = tk.Canvas(self.parent, width=1180, height=605)
        self.frame = tk.Frame(self.canvas)

        self.dataTable()

        self.canvas.create_window(20, 0, anchor='nw', window=self.frame)
        # add the scrollbars
        vbar = tk.Scrollbar(self.parent, orient='vertical', command=self.canvas.yview)
        hbar = tk.Scrollbar(self.parent, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=hbar.set,
                        yscrollcommand=vbar.set,
                        scrollregion=self.canvas.bbox('all'))

        self.canvas.grid(row=0, column=0, sticky='eswn')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')

        self.canvas.bind('<Configure>', self.on_resize)

    def dataTable(self):
        len_FS = App.max_Financial_Securities

        tk.Label(self.frame, text="Financial Securities", width=25, borderwidth="1",relief="solid").grid(row=0, column=0, padx=(400, 0))
        tk.Label(self.frame, text="Variance", width=25, borderwidth="1",relief="solid").grid(row=0, column=1)

        for row in range(len_FS):
            tk.Label(self.frame, text=row + 1, width=25, borderwidth="1", relief="ridge").grid(row=row + 1, column=0, padx=(400, 0))
        
        for row, variance in enumerate(App.portfolio.variance):
            formatted_value = "{:.5E}".format(variance) # convertir en notation scientifique avec 5 chiffres après la virgule
            tk.Label(self.frame, text=formatted_value, width=25, borderwidth="1",relief="ridge").grid(row=row + 1, column=1)
                
    def on_resize(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))