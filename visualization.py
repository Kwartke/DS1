import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pgeocode as pgc

df: pd.DataFrame = pd.read_csv('output/merged.csv', engine='python')

df_merged = df[~np.isinf(df)].copy()
df_merged.dropna(inplace=True)
df_merged = df_merged[(df_merged > 0).all(1)].copy()


pgcodes = pgc.Nominatim('DE')
df_plz = df_merged["plz"].to_numpy()
plz_strings = ["%.i" % number for number in df_plz]
long_lat = pgcodes.query_postal_code(plz_strings)
long_lat = long_lat[['longitude', 'latitude']]

#frames = [df_merged, long_lat]
#result = pd.concat(frames, axis=1)

plt.figure()
ax = plt.gca()
ax.get_yaxis().get_major_formatter().set_scientific(False)
ax.set(xlim=(0, 30), ylim=(0, 300))
plt.scatter(df_merged['avg_Mietpreis_pro_m2'], df_merged['Wohnflaeche__m�_'])
plt.xlabel("Durchschnittlicher Mietpreis pro qm")
plt.ylabel("Wohnfläche")
#plt.show()

plt.figure()
ax = plt.gca()
ax.set(xlim=(0, 5000), ylim=(0, 1000))
ax.get_yaxis().get_major_formatter().set_scientific(False)
plt.scatter(df_merged['avg_Kaufpreis_pro_m2'],df_merged['Wohnflaeche__m�_'])
plt.xlabel("Durchschnittlicher Kaufpreis pro qm")
plt.ylabel("Wohnfläche")
#plt.show()

plt.figure()
ax = plt.gca()
ax.set(xlim=(0, 10), ylim=(0, 40))
plt.scatter(df_merged['Zimmer'],df_merged['avg_Mietpreis_pro_m2'])
plt.xlabel("Anzahl Zimmer")
plt.ylabel("Durchschnittlicher Kaufpreis pro qm")
#plt.show()
