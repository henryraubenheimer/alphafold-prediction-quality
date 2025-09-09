import json
import os

import numpy as np
from sklearn.linear_model import LinearRegression

import helper_functions


X = [] # Features list
y = [] # Target list

with open("./ml_model/train data/ptm.json", "r") as f:
    data = json.load(f)

# Loop through every .pdb file in the directory
for filename in os.listdir("./ml_model/train data"):
    if filename.lower().endswith(".pdb"):

        file_path = os.path.join("./ml_model/train data", filename)
        residue_data = helper_functions.parse_pdb(file_path)

        segments = helper_functions.find_low_confidence_segments(residue_data, threshold=70)
        max_segment = max(segments, key=len)

        # Add features and target to lists
        X.append([
            residue_data.mean(),
            (residue_data < 50).mean() * 100,
            (residue_data < 70).mean() * 100,
            max_segment[1] - max_segment[0]
        ])
        y.append(data[filename[:-4]])

# Train a linear regression model
X = np.array(X)
y = np.array(y)
model = LinearRegression()
model.fit(X, y)

# Save the model
import pickle
with open("regressor_model.pkl", "wb") as f:
    pickle.dump(model, f)
