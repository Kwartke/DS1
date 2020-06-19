import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


df: pd.DataFrame = pd.read_csv('output/merged.csv', engine='python')
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df = df.apply(lambda x: x.fillna(x.mean()))

def build_knn_model(target: str):
    X_train = df.drop(target, axis=1)
    y_train = df[[target]]

    X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.1)

    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train, y_train)
    predictions = knn.predict(X_test)
    print(predictions)

    #evaluate model
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, predictions))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, predictions))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))


build_knn_model('avg_Mietpreis_pro_m2')

