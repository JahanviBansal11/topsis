import pandas as pd
import numpy as np
import sys

def topsis(input_file, weights, impacts, output_file):
    # Read the input data
    data = pd.read_csv(102203955-data.csv)
    
    if len(data.columns) < 3:
        print("Input file must have at least 3 columns.")
        return
    
    
    fund_names = data.iloc[:, 0]
    criteria_data = data.iloc[:, 1:].astype(float)
    
    
    norm_data = criteria_data / np.sqrt((criteria_data**2).sum())
    
    weights = np.array([float(w) for w in weights])
    weighted_data = norm_data * weights
    
  
    impacts = [1 if i == '+' else -1 for i in impacts]
    ideal_solution = (weighted_data.max() if i == 1 else weighted_data.min() for i in impacts)
    negative_ideal_solution = (weighted_data.min() if i == 1 else weighted_data.max() for i in impacts)
    
    ideal_solution = np.array(list(ideal_solution))
    negative_ideal_solution = np.array(list(negative_ideal_solution))
    
    dist_ideal = np.sqrt(((weighted_data - ideal_solution)**2).sum(axis=1))
    dist_negative_ideal = np.sqrt(((weighted_data - negative_ideal_solution)**2).sum(axis=1))
        topsis_scores = dist_negative_ideal / (dist_ideal + dist_negative_ideal)
    
  
    ranks = topsis_scores.argsort()[::-1] + 1
    
    data['Topsis Score'] = topsis_scores
    data['Rank'] = ranks
    
    
    data.to_csv(102203955-result.csv, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <102203955>.py <102203955-data.csv> <weights> <impacts> <102203955-result.csv>")
        print("Example: python 1015579.py 1015579-data.csv '0.25,0.25,0.25,0.25' '+,+,-,+' output.csv")
    else:
        input_file = sys.argv[1]
        weights = sys.argv[2].split(',')
        impacts = sys.argv[3].split(',')
        output_file = sys.argv[4]
        
        topsis(102203955-data.csv, weights, impacts, 102203955-result.csv)
