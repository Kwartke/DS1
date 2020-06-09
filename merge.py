import pandas as pd
import csv

house_data = pd.read_csv("output/cleaned_house_prices.csv")
rent_data = pd.read_csv("output/cleaned_rent.csv")

shared_columns = ["Einbaukueche", 'Garten/_mitnutzung', 'Balkon', 'Wohnflaeche__m²_', 'Zimmer', 'Keller', 'Haustiere_erlaubt']

with open('output/merged.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["plz", "avg_Kaufpreis_pro_m2", "avg_Mietpreis_pro_m2"] + shared_columns)
    for plz in range(10**6):
        houses_in_plz = house_data[house_data["plz"] == plz]
        rent_in_plz = rent_data[rent_data["plz"] == plz]
        if not houses_in_plz.empty and not rent_in_plz.empty:
            try:
                row = [str(plz).zfill(5), houses_in_plz["Preis_pro_m2"].mean(), rent_in_plz["Preis_pro_m2"].mean()]
                for col in shared_columns:
                    value = (houses_in_plz[col].apply(lambda x: float(x)).sum() + rent_in_plz[col].apply(lambda x: float(x)).sum()) / (len(houses_in_plz) + len(rent_in_plz))
                    row.append(value)
                csvwriter.writerow(row)
            except:
                pass