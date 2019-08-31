import tensorflow as tf
import keras
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

# Loading data from the hltv api
data = pd.DataFrame.from_dict(hltv.get_results());

# Encoding all non-numeric values
le = preprocessing.LabelEncoder()
for column in data:
    if data[column].dtype != "int64":
        data[column] = le.fit_transform(list(data[column]));

features = np.array(data.drop(["team1score"], 1).drop(["team2score"], 1));
labels = np.array(data["team1score"] + data["team2score"]);

print(data.head())
