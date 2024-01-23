from typing import List

class Financial_Securities:

    def __init__(self, name, date, open, hight, low, close, volume, ior = None):
        self.name = name
        self.date = date
        self.open = open
        self.hight = hight
        self.low = low
        self.close = close
        self.volume = volume

        if ior is None:
            ior = []
        self.ior = ior

class Portfolio:

    total_dates = []

    def __init__(self, financial_Securities: List[Financial_Securities] = None, covariance = None, variance = None):

        if financial_Securities is None:
            financial_Securities = []
        self.financial_Securities = financial_Securities

        if covariance is None:
            self.covariance = []
        self.covariance = covariance 
        
        if variance is None:
            self.variance = []
        self.variance = variance
