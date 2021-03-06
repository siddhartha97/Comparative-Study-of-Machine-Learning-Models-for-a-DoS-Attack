import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


class RandomForest:

    def __init__(self, df):
        self.df = df
        self.X = pd.DataFrame()
        self.Y = pd.DataFrame()

        self.x_train = pd.DataFrame()
        self.y_train = pd.DataFrame()

        self.x_test = pd.DataFrame()
        self.y_test = pd.DataFrame()

    def preprocessing(self):
        col_rate = self.df["Collision_rate"] < 1
        rec_rate = self.df["Received Rate"] < 100
        final_df = self.df[col_rate & rec_rate]
        self.X = final_df[["Collision_rate", "Received Rate"]]
        self.Y = final_df["Probability"]

    def train_test_split(self):
        self.preprocessing()
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.X, self.Y, test_size=0.4,
                                                                                random_state=123)

    def plot_function(self):
        pass

    def get_best_params(self):
        deep = list(range(2, 17))
        leaf = list(range(2, 19))
        split = list(range(2, 15))

        param_grid = dict(max_depth=deep, min_samples_leaf=leaf, min_samples_split=split)
        c = GridSearchCV(RandomForestRegressor(random_state=1), param_grid, cv=3, scoring='r2',verbose= 3)
        c.fit(self.x_train, self.y_train)

        print("Grid Search best score : ", c.best_score_)

        return c.best_estimator_

    def fit_model(self):
        self.train_test_split()
        print ("Running Model Forest\n")
        rf = RandomForestRegressor(self.get_best_params())
        rf.fit(self.x_train, self.y_train)
        predict = rf.predict(self.x_test)

        return r2_score(predict, self.y_test)
