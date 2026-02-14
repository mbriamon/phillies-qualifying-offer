# MLB 2016 Qualifying Offer Calculator ⚾

> **Hi! I'm Mary!** 👋  
> Thank you so much for this opportunity! I built this app to showcase how I approach data problems and web development. I hope you love exploring it as much as I loved building it!  
> **Go Phils!** 🔴⚪🔵

---

A web application that calculates the 2016 MLB Qualifying Offer by fetching live salary data and computing the average of the top 125 player salaries.

## Features

- **Live Data Fetching**: Pulls fresh salary data from the source URL on each request
- **Accurate Calculation**: Properly handles data cleaning (removes $, $$, $$$, commas, invalid entries)
- **Interactive Visualizations**: Python-powered Plotly charts for salary distribution
- **Percentile Calculator**: Fun widget to see where any salary would rank
- **Beautiful UI**: Phillies-themed interface with the Phanatic!
- **Responsive Design**: Works on desktop, tablet, and mobile

## Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite
- Plotly (for displaying Python-generated charts)
- Custom CSS (Phillies-themed, no UI library needed!)

**Backend:**
- Python 3.12
- Flask + Flask-CORS
- Pandas (data cleaning & analysis)
- Plotly (interactive visualizations)
- BeautifulSoup4 (HTML parsing)

## Project Structure

```
phillies-qualifying-offer/
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── App.css          # Phillies-themed styling
│   │   ├── index.css        # Global styles
│   │   └── main.tsx         # Entry point
│   ├── public/
│   │   └── phanatic.gif     # The star of the show!
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── app.py               # Flask API with data processing
│   └── requirements.txt
└── data_analysis.py         # Standalone Python script (bonus!)
```

## Getting Started

## Prerequisites

Before you begin, make sure you have installed:
- Python 3.10+ (download from python.org)
- Node.js 18+ (download from nodejs.org)

Clone the repository. 

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install all dependencies in the requirements.txt file:
```bash
pip install -r requirements.txt   
```

4. Run the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup - In Another Terminal (Keep the Backend running)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## API Endpoints

### `GET /api/calculate`
Calculates the qualifying offer and returns detailed data including Plotly charts.

**Response:**
```json
{
  "qualifying_offer": 16518594.14,
  "median_salary": 15000000,
  "salary_spread": 24571429,
  "chart": { ... },  // Plotly bar chart JSON
  "pie_chart": { ... },  // Plotly pie chart JSON
  "top_125": [
    {
      "player": "Kershaw, Clayton",
      "salary": 34571429
    },
    ...
  ],
  "valid_salaries": 1173,
  "invalid_salaries": 35,
  "highest_salary": {
    "player": "Kershaw, Clayton",
    "salary": 34571429
  },
  "cutoff_salary": {
    "player": "Bumgarner, Madison",
    "salary": 9950000
  }
}
```

### `GET /api/health`
Health check endpoint.

## Design Decisions

**Why Python for Visualizations?**
- Python gives me more control over complex data transformations
- The backend generates publication-quality charts that the frontend just displays

**Color Scheme:**
- Phillies Red: `#E81828`
- Phillies Blue: `#002D72`
- Blue gradients for charts (from light `#A8C5E0` to dark `#001230`)

**User Experience:**
- Percentile calculator makes it interactive and fun
- Expandable table (top 25 → all 125) keeps the page clean
- Clear stat cards show key metrics at a glance
- Animated Phanatic adds personality! 

## How It Works

1. **Data Fetching**: Backend fetches HTML from the source URL using pandas `read_html()`
2. **Data Cleaning**: Removes `$`, `$$`, `$$$`, commas, converts to numbers, drops invalid entries
3. **Calculation**: Sorts by salary (descending), takes top 125, calculates mean (QO) and median
4. **Visualization**: Creates Plotly charts in Python, sends as JSON to frontend
5. **Display**: React displays data with interactive Plotly charts

## Key Features Explained

- **Median vs Mean**: Shows both to demonstrate understanding of statistical concepts
- **Salary Gap**: Highlights the $24M+ difference between #1 and #125
- **Tier Breakdown**: Pie chart categorizes players into Elite/High Earners/Mid-Tier
- **Percentile Calculator**: Interactive widget where you can input any salary and see where it ranks
- **Data Quality Metrics**: Shows how many invalid entries were removed

## Notes

- Data refreshes with each request (as per requirements)
- Handles edge cases: multiple `$`, missing commas, blank cells, "no salary data" text
- All 125 salaries included in calculation
- Standalone `data_analysis.py` script if you want to run it without the web interface

---

*Built with passion for the Philadelphia Phillies Baseball R&D Team* ⚾❤️