import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("input/immo_data.csv")

binFeatures = ['Balkon', 'noParkSpaces', 'Einbaukueche', 'Keller', 'Haustiere_erlaubt', 'lift',
               'Garten/_mitnutzung']

ignoredFeatures = ["regio1", "picturecount", "pricetrend", "scoutId", "geo_bln", "geo_krs", 'regio2', 'regio3',
                   'date', "description", "condition", "facilities", "street", "streetPlain"]

df = df.rename(columns={"geo_plz": "plz", "heatingType": "Heizungsart", "garden" : "Garten/_mitnutzung", "noRooms": "Zimmer", "hasKitchen": "Einbaukueche",
                        "cellar": "Keller", "livingSpace": "Wohnflaeche__m²_", "petsAllowed": "Haustiere_erlaubt", "balcony": "Balkon"})
# delete unused features
for feature in ignoredFeatures:
    del df[feature]

# convert binary features
for binFeature in binFeatures:
    df.loc[:, binFeature] = df[binFeature].isnull().apply(lambda x: 0 if x else 1)

trainFeatures = []
trainFeatures.extend(binFeatures)
reg = LinearRegression()

matches = pd.isnull(df.loc[:, "totalRent"]).apply(lambda x: not x)
X_train = df.loc[matches[matches].index, trainFeatures]
y_train = df.loc[matches[matches].index, "totalRent"]
reg.fit(X_train, y_train)

# normalize prices
for feature, coeff in zip(trainFeatures, reg.coef_):
    df["totalRent"] -= df[feature] * coeff

df['plz'] = df['plz'].astype(str).str.zfill(5)
df["Preis_pro_m2"] = df["totalRent"] / df["Wohnflaeche__m²_"]
df.to_csv("output/cleaned_rent.csv")
