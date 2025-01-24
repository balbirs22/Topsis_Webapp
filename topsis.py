import pandas as pd
import numpy as np

def topsis(data, weights, impacts):
    weights = np.array([float(w) for w in weights.split(',')])  # Converts weights to float array
    impacts = impacts.split(',')  # Splits impacts into list

    # Normalize the data by dividing each value by the Euclidean norm of its column
    data_normalized = data.apply(lambda x: x / np.sqrt((x**2).sum()), axis=0)

    # Apply weights to the normalized data
    weighted_normalized = data_normalized * weights

    # Calculate the ideal and anti-ideal solutions
    ideal = pd.Series({col: np.max(weighted_normalized[col]) if impact == '+' else np.min(weighted_normalized[col])
                       for col, impact in zip(weighted_normalized.columns, impacts)})
    anti_ideal = pd.Series({col: np.min(weighted_normalized[col]) if impact == '+' else np.max(weighted_normalized[col])
                            for col, impact in zip(weighted_normalized.columns, impacts)})

    # Calculate distances to the ideal and anti-ideal solutions
    dist_ideal = np.sqrt(((weighted_normalized - ideal) ** 2).sum(axis=1))
    dist_anti_ideal = np.sqrt(((weighted_normalized - anti_ideal) ** 2).sum(axis=1))

    # Calculate the TOPSIS score
    score = dist_anti_ideal / (dist_anti_ideal + dist_ideal)

    # Add scores and ranks to the data
    data['Topsis Score'] = score
    data['Rank'] = score.rank(method='min', ascending=False)

    return data
