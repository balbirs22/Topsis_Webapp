import pandas as pd
import numpy as np

def topsis(data, weights, impacts):
    try:
        # Extracting numeric data only, ignoring non-numeric columns like 'Fund Name'
        numeric_data = data.select_dtypes(include=[np.number])

        # Convert weights from string to float and ensure no surrounding whitespace
        weights = np.array([float(w.strip()) for w in weights.split(',')])

        # Strip any surrounding whitespace from impacts and ensure they are strings
        impacts = [i.strip() for i in impacts.split(',')]

        # Normalize the numeric data by dividing each value by the Euclidean norm of its column
        data_normalized = numeric_data.apply(lambda x: x / np.sqrt((x**2).sum()), axis=0)

        # Apply weights to the normalized data
        weighted_normalized = data_normalized.multiply(weights, axis=1)

        # Calculate the ideal and anti-ideal solutions
        ideal = {}
        anti_ideal = {}
        for col, impact in zip(weighted_normalized.columns, impacts):
            if impact == '+':
                ideal[col] = weighted_normalized[col].max()
                anti_ideal[col] = weighted_normalized[col].min()
            elif impact == '-':
                ideal[col] = weighted_normalized[col].min()
                anti_ideal[col] = weighted_normalized[col].max()

        ideal = pd.Series(ideal)
        anti_ideal = pd.Series(anti_ideal)

        # Calculate distances to the ideal and anti-ideal solutions
        dist_ideal = np.sqrt(((weighted_normalized - ideal) ** 2).sum(axis=1))
        dist_anti_ideal = np.sqrt(((weighted_normalized - anti_ideal) ** 2).sum(axis=1))

        # Calculate the TOPSIS score
        score = dist_anti_ideal / (dist_anti_ideal + dist_ideal)

        # Add scores and ranks to the data
        data['Topsis Score'] = score
        data['Rank'] = score.rank(method='min', ascending=False)

        return data
    except Exception as e:
        print("Error in TOPSIS calculation:", e)
        raise e
