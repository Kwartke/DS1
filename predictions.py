import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

df_rent = pd.read_csv("output/cleaned_rent.csv")
df_house = pd.read_csv("output/cleaned_house_prices.csv")
df_merged = pd.read_csv("output/merged.csv", engine="python")

def linear_regression(df_x: pd.DataFrame, column_x: str, df_y: pd.DataFrame, column_y:str, plot: bool):

    df_x.dropna(inplace=True)
    df_y.dropna(inplace=True)

    X = df_x[[column_x]].values.reshape(-1,1)
    y = df_y[[column_y]].values.reshape(-1,1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    lm = linear_model.LinearRegression()
    lm.fit(X_train, y_train)
    y_pred = lm.predict(X_test)

    #compare actual output and predicted values
    df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
    print(df[0:20])

    if(plot == True):
        plt_predicted_values(df)


def plt_predicted_values(df: pd.DataFrame):
    df1 = df.head(50)
    df1.plot(kind='bar', figsize=(12, 8))
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='blue')
    plt.show()


#predict rent(y) based on the number of rooms(x)
linear_regression(df_rent, 'Zimmer', df_rent, 'totalRent', True)
#linear_regression(df_rent, 'Haustiere_erlaubt', df_rent, 'totalRent', True)
