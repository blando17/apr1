import pandas as pd

# Load your dataset
df = pd.read_excel("selected_data.xlsx")

# Keep only necessary categorical columns
columns = ['market', 'dur_stay', 'mode', 'purpose']
formatted = df[columns].dropna().astype(str)

# Combine each row into a comma-separated string
formatted.apply(lambda row: ",".join(row), axis=1).to_csv("formatted_transactions.csv", index=False, header=False)
