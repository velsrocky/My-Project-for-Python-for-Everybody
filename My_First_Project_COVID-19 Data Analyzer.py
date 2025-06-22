import requests
import pandas as pd
import matplotlib.pyplot as plt

# API URL (public COVID-19 data)
API_URL = "https://disease.sh/v3/covid-19/countries"

def fetch_data():
    """Retrieve live COVID-19 data from the API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_data(data):
    """Convert raw API data into a structured DataFrame."""
    if not data:
        return None
    
    processed = []
    for country in data:
        processed.append({
            "Country": country["country"],
            "Cases": country["cases"],
            "Deaths": country["deaths"],
            "Recovered": country["recovered"],
            "Active": country["active"],
        })
    return pd.DataFrame(processed)

def visualize_data(df, metric, top_n=10):
    """Plot top N countries by selected metric."""
    if df is None:
        print("No data to visualize!")
        return
    
    # Sort and select top N countries
    df_sorted = df.sort_values(by=metric, ascending=False).head(top_n)
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted["Country"], df_sorted[metric], color='skyblue')
    plt.title(f"Top {top_n} Countries by COVID-19 {metric}")
    plt.xlabel("Country")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Fetch and process data
    print("Fetching latest COVID-19 data...")
    raw_data = fetch_data()
    df = process_data(raw_data)
    
    if df is None:
        print("Failed to load data. Exiting.")
        return
    
    # User interaction
    while True:
        print("\nCOVID-19 Data Analyzer")
        print("1. Show Top Countries by Cases")
        print("2. Show Top Countries by Deaths")
        print("3. Show Top Countries by Recovered")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == "1":
            visualize_data(df, "Cases")
        elif choice == "2":
            visualize_data(df, "Deaths")
        elif choice == "3":
            visualize_data(df, "Recovered")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()