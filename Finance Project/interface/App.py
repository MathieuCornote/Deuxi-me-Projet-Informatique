import numpy as np
import tkinter as tk
from model.Portfolio import Portfolio, Financial_Securities
from scipy.interpolate import splrep, splev
import tkinter.font as tkFont
from macro.RandomPortfolio import RandomPortfolio
from macro.IOR import IOR
from macro.Covariance import Covariance
from macro.Variance import Variance
import matplotlib.pyplot as plt
from scipy.interpolate import splrep, splev

import tkinter as tk

class App(tk.Tk):

    all_FS : list[Financial_Securities] = []
    portfolio: Portfolio = None
    max_Financial_Securities : int

    def __init__(self, all_FS, max_Financial_Securities):
        tk.Tk.__init__(self)
        App.all_FS = all_FS
        App.max_Financial_Securities = max_Financial_Securities
        self.title("Finance Project")
        width=1200
        height=700
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self._frame = None

        # Changement de fenêtre
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class, *args):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, *args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        myFont = tkFont.Font(weight="bold")
        if App.portfolio is not None:
            tk.Label(self, text="\t\tFinance Project", fg="black", font=myFont).pack(side="top", fill='x', pady=(100, 120))

            tk.Button(self, text="Random Portfolio", width=15, height=5, fg="white", bg="red", font=myFont, command=lambda: self.Button_Random_Portfolio_command(master, "other")).pack(side="bottom", pady=(30, 0), padx=(190, 0))

            tk.Button(self, text="My Portfolio", width=15, height=5, fg="white", bg="green", font=myFont, command=lambda: master.switch_frame(FramePortfolio)).pack(side="left", fill='y', padx=(200, 0))

            tk.Button(self, text="Graphic", width=15, height=5, fg="white", bg="orange", font=myFont, command=lambda: self.Button_Graphique_command(master)).pack(side="right", fill='y', padx=(0, 10))

            tk.Button(self, text="Rate of return", width=15, height=5, fg="white", bg="blue", font=myFont, command=lambda: self.Button_IOR_command(master)).pack(side="left", expand=1, padx=(10, 10))

            tk.Button(self, text="Covariance", width=15, height=5, fg="white", bg="blue", font=myFont, command=lambda: self.Button_Covariance_command(master)).pack(side="left", expand=1, padx=(0, 10))
            
            tk.Button(self, text="Variance", width=15, height=5, fg="white", bg="blue", font=myFont, command=lambda: self.Button_Variance_command(master)).pack(side="left", expand=1, padx=(0, 10))
        else:
            tk.Label(self, text="\t\t\t\t\tFinance Project", fg="black", font=myFont).pack(side="top", fill='x', pady=(100, 100))

            tk.Button(self, text="Random Portfolio", width=45, height=12, fg="white", bg="grey", font=myFont, command=lambda: self.Button_Random_Portfolio_command(master, "first")).pack(side="left", fill='y', padx=(380, 0))


    def Button_Random_Portfolio_command(self, master, state):
        # Initialisation des macros
        macro1 = RandomPortfolio(App.all_FS)
        App.portfolio = macro1.randomPortfolio(App.max_Financial_Securities)
        macro2 = IOR(App.portfolio)
        macro3 = Covariance(App.portfolio)
        macro4 = Variance(App.portfolio)

        # Appel des macros
        macro2.IOR()
        App.portfolio.covariance = macro3.covariance()
        App.portfolio.variance = macro4.variance()

        if state == "first" :
            master.switch_frame(StartPage)

    def Button_IOR_command(self, master):
        master.switch_frame(FrameIOR)

    def Button_Covariance_command(self, master):
        master.switch_frame(FrameCovariance)
        
    def Button_Variance_command(self, master):
        master.switch_frame(FrameVariance)

    def Button_Graphique_command(self, master):
        variances = App.portfolio.variance
        len_FS = len(App.portfolio.financial_Securities)
        
        # Ferme le graphique
        plt.close('all')
        # Créer les données
        x = np.arange(1, len_FS + 1)
        y = variances

        # interpolation de spline
        spl = splrep(x, y)

        # création de la courbe lisse
        x_smooth = np.linspace(x.min(), x.max(), 200)
        y_smooth = splev(x_smooth, spl)

        # Changer les étiquettes de l'axe des x
        fig, ax = plt.subplots()
        ax.set_xticks(x)
        ax.set_xticklabels(x.astype(int))

        fig.set_figwidth(12)
        fig.set_facecolor('#f0f0f0')
        # tracé du graphe
        plt.grid(axis='y', which='major', color='grey', linestyle='-', linewidth=0.5)
        plt.plot(x_smooth, y_smooth, label='Variance', linewidth=2)
        plt.scatter(x, y, color='red')
        plt.xlabel('Titres financiers')
        plt.title('Variance des titres financiers')
        plt.legend()
        plt.show()

class FramePortfolio(tk.Frame):
    
    def __init__(self, master, state ="current"):
        tk.Frame.__init__(self, master)
        self.parent=master
        self.state = state

        if self.state == "random":
            tk.Label(self, text="Random portfolio").pack(side="top", fill="x", pady=5)
            tk.Button(self, text="Return to the menu", command=lambda: [self.canvas.destroy(), vbar.destroy(), hbar.destroy(), master.switch_frame(StartPage)]).pack()
        else:
            tk.Label(self, text="My portfolio").pack(side="top", fill="x", pady=5)
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


        if self.state == "Random":
            
            for column in range(len_FS):
                
                for row in range(len_total_dates):
                    if row < len(App.portfolio.financial_Securities[column].close):
                        tk.Label(self.frame, text=App.portfolio.financial_Securities[column].close[row], width=10, borderwidth="1",
                                relief="ridge").grid(row=row + 2, column=column + 1)
                    else:
                        tk.Label(self.frame, text="--", width=10, borderwidth="1",
                                relief="ridge").grid(row=row + 2, column=column + 1)
        else:
            for column in range(len_FS):
                
                for row in range(len_total_dates):
                    if row < len(App.portfolio.financial_Securities[column].close):
                        tk.Label(self.frame, text=App.portfolio.financial_Securities[column].close[row], width=10, borderwidth="1",
                                relief="ridge").grid(row=row + 2, column=column + 1)
                    else:
                        tk.Label(self.frame, text="--", width=10, borderwidth="1",
                                relief="ridge").grid(row=row + 2, column=column + 1)
                    
    def on_resize(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

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

class FrameCovariance(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.parent=master

        tk.Label(self, text="Covariance Matrix").pack(side="top", fill="x", pady=5)
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

        tk.Label(self.frame, text="Ticker", width=10, borderwidth="1",relief="solid").grid(row=0, column=0)

        for column in range(len_FS):
            tk.Label(self.frame, text=App.portfolio.financial_Securities[column].name, width=10, borderwidth="1", relief="solid").grid(row=0, column=column + 1)
            tk.Label(self.frame, text=App.portfolio.financial_Securities[column].name, width=10, borderwidth="1", relief="solid").grid(row=column + 1, column=0)
        
        for row, listCovar in enumerate(App.portfolio.covariance):
            
            for column, value in enumerate(listCovar):
                if np.isnan(value):
                    tk.Label(self.frame, text="--", width=10, borderwidth="1",relief="ridge").grid(row=row + 1, column=column + 1)
                else:
                    formatted_value = "{:.5E}".format(value) # convertir en notation scientifique avec 5 chiffres après la virgule
                    if row == column:
                        tk.Label(self.frame, text=formatted_value, width=10, borderwidth="1", bg="orange", fg="black", relief="ridge").grid(row=row + 1, column=column + 1)
                    else:
                        tk.Label(self.frame, text=formatted_value, width=10, borderwidth="1",relief="ridge").grid(row=row + 1, column=column + 1)
                
    def on_resize(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))