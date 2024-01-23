import numpy as np
from model.Portfolio import Portfolio

class Variance:
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def variance(self):
        mcv = self.portfolio.covariance
        # Extraction de la diagonale de la matrice de covariance
        variances = np.diagonal(mcv)
        return variances