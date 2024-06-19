import pandas as pd

# Load the CSV file
file_path = r"C:\Users\Morning\Downloads\munich_trans_facade_samples\munich_trans_facade_samples.csv"
df = pd.read_csv(file_path)

# Modify the 'Floor' column
df['Floor'] = df['Floor'] * 2.4 + 502.5

modified_file_path = r'C:\Users\Morning\Downloads\munich_trans_facade_samples\modified_sample.csv'
df.to_csv(modified_file_path, index=False)