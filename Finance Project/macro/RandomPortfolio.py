import random as rd
from model.Portfolio import Financial_Securities, Portfolio
# NYSE_2015_to_2016

class RandomPortfolio:
    
    def __init__(self, all_FS):
        # Liste des titres financiers
        self.all_Financial_Securities = all_FS

    def randomPortfolio(self, max_Financial_Securities):
        # Position ==> Position du titre financier à ajouter au portfolio
        position = 1

        # Remplissage du portfolio avec les titres financiers
        portfolio = Portfolio()
        while position <= max_Financial_Securities:
            # Récupère un titre financier aléatoirement
            FS : Financial_Securities = self.all_Financial_Securities.pop(rd.randint(0, len(self.all_Financial_Securities) - 1))
            portfolio.financial_Securities.append(FS)
            if len(FS.date) > len(Portfolio.total_dates):
                Portfolio.total_dates = FS.date
            position += 1

        return portfolio
