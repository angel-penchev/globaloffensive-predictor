import tensorflow as tf
import keras
import pandas as pd
import numpy as np
import sklearn
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
import requests
import json
from datetime import datetime, timedelta
from lib.flatten_json import flatten_json

# Loading data from the API / example_data.json if the API is unavailable
try:
    response = requests.get(
        "http://localhost:3000/results/detailed?startDate=" + (datetime.today() - timedelta(days = 30)).strftime("%Y-%m-%d") + "&endDate=" + datetime.today().strftime("%Y-%m-%d")
    );
    data = response.json();
except:
    print("[Error] - HLTV API could not be reached. Please make sure the Node JS serever is up and running...");
    data = json.load(open("./data/example_data.json"));

# Flattening the json data and parsing into pandas table
flattened_data = []
for entry in data:
    flattened_data.append(flatten_json(entry));

le = preprocessing.LabelEncoder();
pd_data = pd.DataFrame.from_dict(flattened_data);
pd_data = pd_data[[
    # "team1_id",
    # "team2_id",
    # "event_id",
    "playerStats_team1_0_id",
    "playerStats_team1_1_id",
    "playerStats_team1_2_id",
    "playerStats_team1_3_id",
    "playerStats_team1_4_id",
    "playerStats_team2_0_id",
    "playerStats_team2_1_id",
    "playerStats_team2_2_id",
    "playerStats_team2_3_id",
    "playerStats_team2_4_id",
    "map"
]]
pd_data["map"] = le.fit_transform(list(pd_data["map"]));
print(pd_data.head());

# Setting the parameters and the lable to predict
predict = "map";
x = np.array(pd_data.drop([predict], 1));
y = np.array(pd_data[predict]);

# Separating training data from test data
test_train_data_ratio = 1 / 10;
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = test_train_data_ratio);

model = KNeighborsClassifier(n_neighbors=9)
model.fit(x_train, y_train);
acc = model.score(x_test, y_test);

print("Model accuracy: ", acc, "%");

# Getting a list of all the predictions and their real y
predictions = model.predict(x_test) 
# print(model.predict_proba(x_test));
for x in range(len(predictions)):
    print("[Prediction]: %d ; [Actual]: %d" % (predictions[x], y_test[x]))