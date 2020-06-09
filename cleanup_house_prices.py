import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_json("input/houses.json")

binFeatures = ['WG_geeignet', 'Dachboden', 'Moebliert/Teilmoebliert', 'Terrasse', 'Einliegerwohnung', 'Balkon',
               'Keller', 'Einbaukueche', 'Denkmalobjekt', 'Garten/_mitnutzung', 'Dusche', 'Barrierefrei', 'Badewanne',
               'Gaeste_WC', 'Garage/Stellplatz', 'Haustiere_erlaubt', 'Aktuell_vermietet']

ignoredFeatures = ["adid", "abtest", "posterid", "yo_m", "yo_s", "elasticSearch", 'kw', 'Verfuegbar_ab_Jahr',
                   'Verfuegbar_ab_Monat']

# delete unused features
for feature in ignoredFeatures:
    del df[feature]

# convert binary features
for binFeature in binFeatures:
    df.loc[:, binFeature] = df[binFeature].isnull().apply(lambda x: 0 if x else 1)

trainFeatures = []
trainFeatures.extend(binFeatures)
reg = LinearRegression()

matches = pd.isnull(df.loc[:, "ExactPreis"]).apply(lambda x: not x)
X_train = df.loc[matches[matches].index, trainFeatures]
y_train = df.loc[matches[matches].index, "ExactPreis"]
reg.fit(X_train, y_train)

# normalize prices
for feature, coeff in zip(trainFeatures, reg.coef_):
    df["Preis"] -= df[feature] * coeff

df['plz'] = df['plz'].astype(str).str.zfill(5)
df["Preis_pro_m2"] = df["Preis"] / df["Wohnflaeche__m²_"]
df.to_csv("output/cleaned_house_prices.csv")
