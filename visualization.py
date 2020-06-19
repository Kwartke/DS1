import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pgeocode as pgc

df: pd.DataFrame = pd.read_csv('output/merged.csv', engine='python')

df_merged = df[~np.isinf(df)].copy()
df_merged.dropna(inplace=True)

pgcodes = pgc.Nominatim('DE')
df_plz = df_merged["plz"].to_numpy()
plz_strings = ["%.i" % number for number in df_plz]
long_lat = pgcodes.query_postal_code(plz_strings)
long_lat = long_lat[['longitude', 'latitude']]

frames = [df_merged, long_lat]
result = pd.concat(frames, axis=1)

print(result['Zimmer'])

plt.figure()
plt.plot(result[['latitude', 'longitude']])
plt.ylabel('Longitude', fontsize=12)
plt.xlabel('Latitude', fontsize=12)
#plt.draw()

plt.figure()
plt.scatter(x=result['avg_Mietpreis_pro_m2'], y=result['Wohnflaeche__m�_'])
ax = plt.gca()
ax.get_yaxis().get_major_formatter().set_scientific(False)
plt.scatter(result['avg_Mietpreis_pro_m2'], result['longitude'])
plt.title("Mietpreis_pro_m2 vs Ort")
#plt.draw()

plt.figure()
plt.scatter(result['avg_Mietpreis_pro_m2'], result['latitude'])
plt.xlabel("Price")
plt.ylabel('Latitude')
plt.title("Latitude vs Mietpreis")
#plt.show()

plt.figure()
plt.scatter(result['Zimmer'], result['avg_Mietpreis_pro_m2'])
plt.title("Mietpreis_pro_m2 und Anzahl der Zimmer")
plt.xlabel("Zimmer")
plt.ylabel("Mietpreis")
#plt.draw()

plt.scatter(x=result['avg_Mietpreis_pro_m2'],y=result['Wohnflaeche__m�_'])
ax = plt.gca()
ax.get_yaxis().get_major_formatter().set_scientific(False)
#plt.draw()

plt.scatter(result['avg_Mietpreis_pro_m2'],result['longitude'])
plt.title("Mietpreis_pro_m2 vs Ort")


plt.scatter(result['avg_Mietpreis_pro_m2'],result['latitude'])
plt.xlabel("Price")
plt.ylabel('Latitude')
plt.title("Latitude vs Mietpreis")

plt.scatter(result['Zimmer'],result['avg_Mietpreis_pro_m2'])
plt.title("Mietpreis_pro_m2 und Anzahl der Zimmer")
plt.xlabel("Zimmer")
plt.ylabel("Mietpreis")
#plt.show()
