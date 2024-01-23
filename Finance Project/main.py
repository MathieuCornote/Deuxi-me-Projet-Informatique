from interface.App import App
from Data.Data_extractor import Data_extractor
from interface.LoadingScreen import LoadingScreen

# Nom du fichier avec les données du marché
file = "Data/NYSE_2015_to_2016.xlsx"

# max_Financial_Securities ==> Nombre de titres financiers pouvant être contenu dans le portfolio au maximum
max_Financial_Securities = 30

# max_Values ==> Nombre de jour où les données des titres financiers seront récupéres
max_Values = 100 # 0 ==> Tous les jours (risque de crash + impossibilié de réalisation de la variance dû à un manque de données), entre 1 et 100 conseillé

if __name__ == "__main__":
    loadingData = LoadingScreen()
    extractor = Data_extractor()
    all_FS = extractor.extract_data(file, max_Values)
    app = App(all_FS, max_Financial_Securities)
    app.mainloop()

