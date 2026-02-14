from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

def fetch_salary_data():
    """Fetch the salary data from the website."""
    url = 'https://questionnaire-148920.appspot.com/swe/data.html'
    tables = pd.read_html(url)
    df = tables[0]
    return df

def clean_salary_column(df):
    """Clean the Salary column and remove invalid entries."""
    # Convert to string first
    df['Salary'] = df['Salary'].astype(str)
    
    # Remove ALL dollar signs (handles $, $$, $$$)
    df['Salary'] = df['Salary'].str.replace(r'\$+', '', regex=True)
    
    # Remove commas
    df['Salary'] = df['Salary'].str.replace(',', '', regex=False)
    
    # Convert to numbers (anything that can't convert becomes NaN)
    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
    
    # Count invalid entries before dropping
    invalid_count = df['Salary'].isna().sum()
    
    # Drop rows with NaN (missing/invalid salaries)
    df = df.dropna(subset=['Salary'])
    
    return df, invalid_count

def calculate_qualifying_offer(df):
    """Calculate the MLB qualifying offer from top 125 salaries."""
    # Sort by salary, highest first
    df = df.sort_values('Salary', ascending=False).reset_index(drop=True)
    
    # Get top 125
    top_125 = df.head(125)
    
    # Calculate average (qualifying offer)
    qualifying_offer = top_125['Salary'].mean()
    
    # Calculate additional stats
    median_salary = top_125['Salary'].median()
    salary_spread = top_125.iloc[0]['Salary'] - top_125.iloc[124]['Salary']
    
    return qualifying_offer, top_125, median_salary, salary_spread


def create_salary_distribution_chart(top_125):
    """Create an interactive Plotly chart showing salary distribution."""
    
    # Define salary ranges
    def get_salary_range(salary):
        if salary >= 30000000:
            return '$30M+'
        elif salary >= 25000000:
            return '$25M-$30M'
        elif salary >= 20000000:
            return '$20M-$25M'
        elif salary >= 15000000:
            return '$15M-$20M'
        elif salary >= 10000000:
            return '$10M-$15M'
        else:
            return 'Under $10M'
    
    # Add range column
    top_125['Range'] = top_125['Salary'].apply(get_salary_range)
    
    # Count players in each range
    range_counts = top_125['Range'].value_counts().reset_index()
    range_counts.columns = ['Range', 'Count']
    
    # Define proper order (low to high)
    range_order = ['Under $10M', '$10M-$15M', '$15M-$20M', '$20M-$25M', '$25M-$30M', '$30M+']
    range_counts['Range'] = pd.Categorical(range_counts['Range'], categories=range_order, ordered=True)
    range_counts = range_counts.sort_values('Range')
    
    # Create bar chart
    fig = go.Figure()
    
    # Phillies blue gradient (light to dark)
    colors = ['#A8C5E0', '#6B8BC3', '#3B5998', '#002D72', '#001B44', '#001230']
    
    fig.add_trace(go.Bar(
        x=range_counts['Range'],
        y=range_counts['Count'],
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        text=range_counts['Count'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{y} players<extra></extra>'
    ))
    
    # Update layout with Phillies theme
    fig.update_layout(
        title={
            'text': '📊 Salary Distribution - Top 125 MLB Players',
            'font': {'size': 24, 'color': '#002D72', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Salary Range',
        yaxis_title='Number of Players',
        plot_bgcolor='rgba(249, 250, 251, 0.5)',
        paper_bgcolor='white',
        font=dict(family='Inter, sans-serif', size=14, color='#4B5563'),
        height=500,
        margin=dict(t=80, b=80, l=60, r=40),
        hovermode='x unified',
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            gridcolor='rgba(229, 231, 235, 0.8)',
            tickfont=dict(size=12)
        )
    )
    
    # Convert to JSON for frontend
    return json.loads(fig.to_json())


def create_pie_chart(top_125):
    """Create a pie chart showing salary tier breakdown."""
    
    def get_tier(salary):
        if salary >= 25000000:
            return 'Elite ($25M+)'
        elif salary >= 15000000:
            return 'High Earners ($15M-$25M)'
        else:
            return 'Mid-Tier ($10M-$15M)'
    
    top_125['Tier'] = top_125['Salary'].apply(get_tier)
    tier_counts = top_125['Tier'].value_counts()
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=tier_counts.index,
        values=tier_counts.values,
        hole=0.4,  # Donut chart
        marker=dict(colors=['#E81828', '#002D72', '#6B8BC3']),
        textposition='none',  # Remove text from slices
        hovertemplate='<b>%{label}</b><br>%{value} players<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '🥧 Salary Tier Breakdown',
            'font': {'size': 20, 'color': '#002D72'},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=400,
        paper_bgcolor='white',
        font=dict(family='Inter, sans-serif', size=12),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return json.loads(fig.to_json())

@app.route('/api/calculate', methods=['GET'])
def calculate():
    """API endpoint to calculate the qualifying offer."""
    try:
        print("Starting calculation...")
        
        # Fetch and clean data
        print("Fetching data...")
        df = fetch_salary_data()
        print(f"Fetched {len(df)} rows")
        
        total_rows = len(df)
        
        print("Cleaning data...")
        df_clean, invalid_count = clean_salary_column(df)
        valid_count = len(df_clean)
        print(f"{valid_count} valid salaries, {invalid_count} invalid")
        
        # Calculate qualifying offer
        print("  Calculating QO...")
        qo, top_125, median_salary, salary_spread = calculate_qualifying_offer(df_clean)
        print(f"   QO calculated: ${qo:,.2f}")
        print(f"   Median: ${median_salary:,.2f}")
        print(f"   Spread: ${salary_spread:,.2f}")
        
        # Generate Plotly charts
        print("Generating charts...")
        chart_json = create_salary_distribution_chart(top_125.copy())
        pie_chart_json = create_pie_chart(top_125.copy())
        print("Charts generated")
        
        # Prepare response data
        response = {
            'qualifying_offer': float(qo),
            'median_salary': float(median_salary),
            'salary_spread': float(salary_spread),
            'chart': chart_json,  # Plotly bar chart JSON
            'pie_chart': pie_chart_json,  # Plotly pie chart JSON
            'top_125': [
                {
                    'player': str(row['Player']),
                    'salary': int(row['Salary'])  # Convert to Python int
                }
                for _, row in top_125.iterrows()
            ],
            'valid_salaries': int(valid_count),  # Convert to Python int
            'invalid_salaries': int(invalid_count),  # Convert to Python int
            'total_rows': int(total_rows),  # Convert to Python int
            'highest_salary': {
                'player': str(top_125.iloc[0]['Player']),
                'salary': int(top_125.iloc[0]['Salary'])  # Convert to Python int
            },
            'cutoff_salary': {
                'player': str(top_125.iloc[124]['Player']),
                'salary': int(top_125.iloc[124]['Salary'])  # Convert to Python int
            }
        }
        
        print("Sending response to frontend")
        return jsonify(response)
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)