from model.Portfolio import Portfolio
import numpy as np

class Covariance:

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def covariance(self):
        len_FS = len(self.portfolio.financial_Securities)
        # Création de la matrice de covariance
        matrix_covariance = np.zeros((len_FS, len_FS))
        # Comparaison de chaque itération de colonne avec la suivante
        for i in range(len_FS):
            column1 = self.portfolio.financial_Securities[i].ior

            for j in range(i+1):
                column2 = self.portfolio.financial_Securities[j].ior

                if len(column1) == len(column2):
                    # Calcul de la covariance entre la colonne 1 et la colonne 2
                    covar = np.cov(column1, column2)[0][1]
                else:
                    covar = np.nan
            
                matrix_covariance[i, j] = covar
                matrix_covariance[j, i] = covar

        return matrix_covariance
