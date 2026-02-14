import pandas as pd

def fetch_salary_data():
    """
    Fetch the salary data from the website.
    Returns a pandas DataFrame with Player, Salary, Year, Level columns.
    """
    url = 'https://questionnaire-148920.appspot.com/swe/data.html'
    
    # Read all tables from the HTML page
    tables = pd.read_html(url)
    
    # Get the first table (there's only one)
    df = tables[0]
    
    print(f"Fetched {len(df)} rows from {url}")
    return df


def clean_salary_column(df):
    """
    Clean the Salary column by:
    1. Removing all dollar signs ($, $$, $$$)
    2. Removing commas
    3. Converting to numbers
    4. Removing invalid entries (blanks, "no salary data", etc)
    
    Returns a cleaned DataFrame with only valid salaries.
    """
    print("\n🧹 Cleaning salary data...")
    
    # Convert to string first
    df['Salary'] = df['Salary'].astype(str)
    
    # Remove ALL dollar signs (handles $, $$, $$$)
    df['Salary'] = df['Salary'].str.replace(r'\$+', '', regex=True)
    
    # Remove commas
    df['Salary'] = df['Salary'].str.replace(',', '', regex=False)
    
    # Convert to numbers (anything that can't convert becomes NaN)
    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
    
    # Count how many valid salaries we have before dropping
    valid_count_before = len(df)
    
    # Drop rows with NaN (missing/invalid salaries)
    df = df.dropna(subset=['Salary'])
    
    invalid_count = valid_count_before - len(df)
    print(f"   Removed {invalid_count} invalid/missing salaries")
    print(f"   {len(df)} valid salaries remaining")
    
    return df


def calculate_qualifying_offer(df):
    """
    Calculate the MLB qualifying offer:
    - Sort salaries highest to lowest
    - Take top 125 salaries
    - Calculate the average
    
    Returns the qualifying offer amount and the top 125 DataFrame.
    """
    print("\n💰 Calculating qualifying offer...")
    
    # Sort by salary, highest first
    df = df.sort_values('Salary', ascending=False).reset_index(drop=True)
    
    # Get top 125
    top_125 = df.head(125)
    
    # Calculate average
    qualifying_offer = top_125['Salary'].mean()
    
    print(f"   Top 125 players selected")
    print(f"   Highest salary: ${top_125.iloc[0]['Salary']:,.0f} ({top_125.iloc[0]['Player']})")
    print(f"   125th salary: ${top_125.iloc[124]['Salary']:,.0f} ({top_125.iloc[124]['Player']})")
    
    return qualifying_offer, top_125


def main():
    """
    Main function that runs the whole process.
    """
    print("=" * 60)
    print("MLB 2016 QUALIFYING OFFER CALCULATOR")
    print("=" * 60)
    
    # Step 1: Fetch the data
    df = fetch_salary_data()
    
    # Step 2: Clean the data
    df_clean = clean_salary_column(df)
    
    # Step 3: Calculate the qualifying offer
    qo, top_125 = calculate_qualifying_offer(df_clean)
    
    # Step 4: Display results
    print("\n" + "=" * 60)
    print(f"2016 QUALIFYING OFFER: ${qo:,.2f}")
    print("=" * 60)
    
    # Optional: Show top 25 players
    print("\nTop 25 Players:")
    print("-" * 60)
    for i in range(25):
        player = top_125.iloc[i]['Player']
        salary = top_125.iloc[i]['Salary']
        print(f"{i+1:2d}. {player:30s} ${salary:>12,.0f}")
    
    return qo, top_125


# Run the program
if __name__ == "__main__":
    qualifying_offer, top_125_players = main()