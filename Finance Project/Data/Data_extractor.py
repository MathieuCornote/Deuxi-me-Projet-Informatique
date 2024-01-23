import pandas as pd
from model.Portfolio import Financial_Securities

class Data_extractor:

    def __init__(self):
        self.df = None

    def convertDateFormat(self, timestamp):
        # Récupérer les dates avec le format "y-m-d"
        return timestamp.date()
    
    def extract_data(self, file, maxValues):
        # Lire le fichier Excel et stocker les données dans un DataFrame
        self.df = pd.read_excel(file)

        # Grouper les données par les nom des titre financiers
        grouped = self.df.groupby('Name')

        # Création des objets "financial_Securities" à partir des données récupérées
        if maxValues != 0:
            all_Financial_Securities = []
            for name, group in grouped:
                name_FS = name
                date_FS = [self.convertDateFormat(date) for date in group['date'].tolist()[:maxValues]]
                open_FS = group['open'].tolist()[:maxValues]
                hight_FS = group['high'].tolist()[:maxValues]
                low_FS = group['low'].tolist()[:maxValues]
                close_FS = group['close'].tolist()[:maxValues]
                volume_FS = group['volume'].tolist()[:maxValues]
                financial_Securities = Financial_Securities(name_FS, date_FS, open_FS, hight_FS, low_FS, close_FS, volume_FS)
                all_Financial_Securities.append(financial_Securities)
        else:
            # Récupère les données pour tous les jours
            all_Financial_Securities = []
            for name, group in grouped:
                name_FS = name
                date_FS = [self.convertDateFormat(date) for date in group['date'].tolist()]
                open_FS = group['open'].tolist()
                hight_FS = group['high'].tolist()
                low_FS = group['low'].tolist()
                close_FS = group['close'].tolist()
                volume_FS = group['volume'].tolist()
                financial_Securities = Financial_Securities(name_FS, date_FS, open_FS, hight_FS, low_FS, close_FS, volume_FS)
                all_Financial_Securities.append(financial_Securities)
        return all_Financial_Securities
