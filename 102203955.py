
import pandas as pd
import numpy as np
import sys

def topsis(input_file, weights, impacts, output_file):
    try:
       
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except Exception as e:
        print(f"Error: Unable to read the file. {e}")
        return
    
    if len(data.columns) < 3:
        print("Error: Input file must contain at least three columns.")
        return
    
    fund_names = data.iloc[:, 0]
    try:
        criteria_data = data.iloc[:, 1:].astype(float)
    except ValueError:
        print("Error: All criteria columns must contain numeric values only.")
        return
    
    if len(weights) != criteria_data.shape[1]:
        print("Error: Number of weights must match the number of criteria columns.")
        return
    try:
        weights = np.array([float(w) for w in weights])
    except ValueError:
        print("Error: All weights must be numeric.")
        return
    
    if len(impacts) != criteria_data.shape[1]:
        print("Error: Number of impacts must match the number of criteria columns.")
        return
    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be '+' or '-'.")
        return
    
    norm_data = criteria_data / np.sqrt((criteria_data**2).sum())
    weighted_data = norm_data * weights
    
    impacts = [1 if i == '+' else -1 for i in impacts]
    ideal_solution = []
    negative_ideal_solution = []

    for i, impact in enumerate(impacts):
        if impact == 1:  # Positive impact
            ideal_solution.append(weighted_data.iloc[:, i].max())
            negative_ideal_solution.append(weighted_data.iloc[:, i].min())
        else:  # Negative impact
            ideal_solution.append(weighted_data.iloc[:, i].min())
            negative_ideal_solution.append(weighted_data.iloc[:, i].max())

    ideal_solution = np.array(ideal_solution)
    negative_ideal_solution = np.array(negative_ideal_solution)
    
    dist_ideal = np.sqrt(((weighted_data - ideal_solution)**2).sum(axis=1))
    dist_negative_ideal = np.sqrt(((weighted_data - negative_ideal_solution)**2).sum(axis=1))
    
    topsis_scores = dist_negative_ideal / (dist_ideal + dist_negative_ideal)
    ranks = topsis_scores.argsort()[::-1] + 1
    
    data['Topsis Score'] = topsis_scores
    data['Rank'] = ranks
    
    try:
        data.to_csv(output_file, index=False)
        print(f"Results saved to '{output_file}'")
    except Exception as e:
        print(f"Error: Unable to save results to the file. {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <RollNumber>.py <input_file> <weights> <impacts> <output_file>")
        print("Example: python 1015579.py 1015579-data.csv '1,1,1,1' '+,+,-,+' 1015579-result.csv")
    else:
        input_file = sys.argv[1]
        weights = sys.argv[2].split(',')
        impacts = sys.argv[3].split(',')
        output_file = sys.argv[4]
        
        topsis(input_file, weights, impacts, output_file)

