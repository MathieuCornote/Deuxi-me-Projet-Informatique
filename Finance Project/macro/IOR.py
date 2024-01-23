from model.Portfolio import Portfolio

class IOR:
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def IOR(self):
        for FS in self.portfolio.financial_Securities:
            # Premier taux à 0 car il s'agit d'une observation de clôture
            all_IOR = [0]
            for i in range(1, len(FS.close)):
                close1 = FS.close[i - 1]
                close2 = FS.close[i]
                # Calcul de du taux de rentabilité entre la clôture 1 et la clôture 2
                if close1 is not None and close2 is not None:
                    ior = (close2 / close1) - 1
                    if ior == 0.0:
                        ior = 0
                else:
                    ior = None
                all_IOR.append(ior)
            FS.ior = all_IOR