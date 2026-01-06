# Step 1: Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# Step 2: Load CSV in three ways
# ------------------------------

# (a) Upload from local computer
from google.colab import files

def load_from_local():
    uploaded = files.upload()  # lets user pick file
    for fn in uploaded.keys():
        df = pd.read_csv(fn)
        return df

# (b) Get a URL from user input
def load_from_user_url():
    url = input("Enter CSV file URL: ")
    df = pd.read_csv(url)
    return df

# (c) Hardcode a URL
def load_from_code():
    url = "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"  # Example dataset
    df = pd.read_csv(url)
    return df

# ------------------------------
# Step 3: Display DataFrame info
# ------------------------------

def explore_dataframe(df):
    print("\n--- Data Preview ---")
    print(df.head(2))  # first two rows
    print("\n--- Column Names ---")
    print(list(df.columns))  # store as list
    return list(df.columns)

# ------------------------------
# Step 4: Convert columns to NumPy
# ------------------------------

def get_numpy_arrays(df, col1, col2=None):
    x = df[col1].to_numpy()
    if col2:
        y = df[col2].to_numpy()
        return x, y
    return x

# ------------------------------
# Step 5: Plotting functions
# ------------------------------

def plot_data(df, col1, col2=None, kind="scatter"):
    if col2:
        x, y = get_numpy_arrays(df, col1, col2)
        if kind == "scatter":
            plt.scatter(x, y)
            plt.xlabel(col1); plt.ylabel(col2)
            plt.title(f"Scatter plot of {col1} vs {col2}")
        elif kind == "line":
            plt.plot(x, y)
            plt.xlabel(col1); plt.ylabel(col2)
            plt.title(f"Line graph of {col1} vs {col2}")
    else:
        x = get_numpy_arrays(df, col1)
        if kind == "line":
            plt.plot(x)
            plt.title(f"Line graph of {col1}")
        else:
            plt.scatter(range(len(x)), x)
            plt.title(f"Scatter plot of {col1}")
        plt.xlabel("Index"); plt.ylabel(col1)

    plt.grid(True)
    plt.show()

# ------------------------------
# Step 6: Menu for user
# ------------------------------

def data_graph_explorer():
    print("\n--- Data Graph Explorer ---")
    print("1. Upload CSV from local computer")
    print("2. Load CSV from user-provided URL")
    print("3. Load CSV from hardcoded URL")
    choice = input("Choose an option (1/2/3): ")

    if choice == "1":
        df = load_from_local()
    elif choice == "2":
        df = load_from_user_url()
    else:
        df = load_from_code()

    cols = explore_dataframe(df)

    print("\nChoose one or two columns to graph.")
    col1 = input(f"Enter first column name (from {cols}): ")
    col2 = input("Enter second column name (or leave blank): ")

    kind = input("Graph type? (scatter/line): ")

    if col2.strip() == "":
        plot_data(df, col1, kind=kind)
    else:
        plot_data(df, col1, col2, kind)

# ------------------------------
# Run Program
# ------------------------------

data_graph_explorer()
