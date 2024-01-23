import tkinter as tk
from interface.App import App


class FrameIOR(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.parent=master

        tk.Label(self, text="Rate of return").pack(side="top", fill="x", pady=5)
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
        total_dates = App.portfolio.total_dates
        len_total_dates = len(total_dates)

        tk.Label(self.frame, text="Number", width=20, borderwidth="1",relief="solid").grid(row=0, column=0)
        tk.Label(self.frame, text="Ticker", width=20, borderwidth="1",relief="solid").grid(row=1, column=0)

        for column in range(len_FS):
            tk.Label(self.frame, text=column + 1, width=10, borderwidth="1", relief="solid").grid(row=0, column=column + 1)
            tk.Label(self.frame, text=App.portfolio.financial_Securities[column].name, width=10, borderwidth="1", relief="solid").grid(row=1, column=column + 1)

        for index, date in enumerate(total_dates):
                    tk.Label(self.frame, text=date, width=20, borderwidth="1", relief="ridge").grid(row=index + 2, column=0)

        for column in range(len_FS):
            
            for row in range(len_total_dates):
                if row < len(App.portfolio.financial_Securities[column].ior):
                    ior = round(App.portfolio.financial_Securities[column].ior[row], 6)
                    if ior > 0:
                        tk.Label(self.frame, text=ior, width=10, borderwidth="1", relief="ridge", fg="red").grid(row=row + 2, column=column + 1)
                    elif ior < 0:
                        tk.Label(self.frame, text=ior, width=10, borderwidth="1", relief="ridge", fg="green").grid(row=row + 2, column=column + 1)
                    else:
                        tk.Label(self.frame, text=ior, width=10, borderwidth="1", relief="ridge").grid(row=row + 2, column=column + 1)
                else:
                    tk.Label(self.frame, text="--", width=10, borderwidth="1", relief="ridge").grid(row=row + 2, column=column + 1)

    def on_resize(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))