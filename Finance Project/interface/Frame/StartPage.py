import numpy as np
import tkinter as tk
import tkinter.font as tkFont
from macro.RandomPortfolio import RandomPortfolio
from macro.IOR import IOR
from macro.Covariance import Covariance
from macro.Variance import Variance
import matplotlib.pyplot as plt
from scipy.interpolate import splrep, splev
from interface.App import 
from Interface.Frame.FramePortfolio import FramePortfolio
from Interface.Frame.FrameIOR import FrameIOR
from Interface.Frame.FrameCovariance import FrameCovariance
from Interface.Frame.FrameVariance import FrameVariance


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