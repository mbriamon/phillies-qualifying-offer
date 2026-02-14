# MLB 2016 Qualifying Offer Calculator

A web application that calculates the 2016 MLB Qualifying Offer by fetching live salary data and computing the average of the top 125 player salaries.

Built for the Philadelphia Phillies Baseball R&D Team.

## Features

- **Live Data Fetching**: Pulls fresh salary data from the source URL on each request
- **Accurate Calculation**: Properly handles data cleaning (removes $, $$, $$$, commas, invalid entries)
- **Beautiful UI**: Phillies-themed interface with red, white, and blue colors
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Data Visualization**: Shows top 25 players and key statistics

## 🛠 Tech Stack

**Frontend:**
- React 18
- TypeScript
- Vite
- CSS3 (custom styling, no UI library)

**Backend:**
- Python 3.10+
- Flask
- Pandas
- BeautifulSoup4

## 📁 Project Structure

```
phillies-qualifying-offer/
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── App.css          # Phillies-themed styling
│   │   ├── index.css        # Global styles
│   │   └── main.tsx         # Entry point
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/
│   ├── app.py               # Flask API
│   └── requirements.txt
└── data_analysis.py           # Standalone Python script
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

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
Calculates the qualifying offer and returns detailed data.

**Response:**
```json
{
  "qualifying_offer": 16518594.14,
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

**Color Scheme:**
- Primary Red: `#E81828` (Phillies Red)
- Primary Blue: `#002D72` (Phillies Blue)
- Clean white backgrounds with subtle shadows
- Gradient accents for visual interest

**Typography:**
- Inter font family for modern, clean look
- Bold weights for numbers and important info
- Proper hierarchy with sizing

**Layout:**
- Card-based design for easy scanning
- Responsive grid for stats
- Prominent display of the qualifying offer
- Table for top 25 players

## How It Works

1. **Data Fetching**: The backend fetches HTML table from the source URL
2. **Data Cleaning**: Removes invalid entries, cleans currency formatting
3. **Calculation**: Sorts salaries, takes top 125, calculates average
4. **Display**: Frontend shows results with beautiful visualizations

## Notes

- Data refreshes with each request (as per requirements)
- Handles various data issues: multiple $, missing commas, blank cells
- All 125 salaries are included in the average calculation
- Invalid entries are properly filtered out

## Deployment

### Deploy to Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Configure build settings:
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. Deploy backend separately (Railway, Render, or AWS)
5. Update frontend API URL in production
