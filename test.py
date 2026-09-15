import sys
import os

# Add the /github/blocktrack directory to the Python path
blocktrack_path = os.path.join(os.path.dirname(__file__), 'github', 'blocktrack')
sys.path.append(blocktrack_path)

from data_production import load_data  # Assuming data_production.py has a load_data function
from gha_index import gha_index        # Assuming gha_index.py has gha_index function

def main():
    # Load your data using data_production.py's function
    data = load_data()

    # Compute the GHA index using the imported function
    gha_result = gha_index(data)

    # Print or process the result as needed
    print("GHA Index Result:", gha_result)

if __name__ == "__main__":
    main()