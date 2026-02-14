import { useState, useEffect } from 'react';
import './App.css';
import Plot from 'react-plotly.js';

interface PlayerSalary {
  player: string;
  salary: number;
}

interface QOData {
  qualifying_offer: number;
  median_salary: number;
  salary_spread: number;
  chart: any;  // Plotly bar chart JSON
  pie_chart: any;  // Plotly pie chart JSON
  top_125: PlayerSalary[];
  valid_salaries: number;
  invalid_salaries: number;
  highest_salary: PlayerSalary;
  cutoff_salary: PlayerSalary;
}

function App() {
  const [data, setData] = useState<QOData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(false);
  const [userSalary, setUserSalary] = useState<string>('');

  const fetchQualifyingOffer = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/calculate');
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQualifyingOffer();
  }, []);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatCurrencyDetailed = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount);
  };

  const calculatePercentile = (salary: number) => {
    if (!data) return null;
    
    const higherCount = data.top_125.filter(p => p.salary > salary).length;
    const percentile = ((125 - higherCount) / 125) * 100;
    const rank = higherCount + 1;
    
    return { percentile, rank };
  };

  const handleSalaryCheck = () => {
    const salary = parseFloat(userSalary.replace(/,/g, ''));
    if (isNaN(salary) || salary <= 0) return null;
    return calculatePercentile(salary);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <img 
              src="/phanatic.gif" 
              alt="Phillie Phanatic"
              className="phanatic-icon"
            />
            <div>
              <h1 className="title">MLB Qualifying Offer Calculator</h1>
              <p className="subtitle">2016 Season • Top 125 Salaries</p>
            </div>
          </div>
          <button 
            className="refresh-button" 
            onClick={fetchQualifyingOffer}
            disabled={loading}
          >
            <span className="refresh-icon">🔄</span>
            {loading ? 'Loading...' : 'Refresh Data'}
          </button>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          {error && (
            <div className="error-card">
              <span className="error-icon">⚠️</span>
              <p>{error}</p>
            </div>
          )}

          {loading && !data && (
            <div className="loading-card">
              <div className="spinner"></div>
              <p>Fetching fresh salary data...</p>
            </div>
          )}

          {data && (
            <>
              {/* Main QO Card */}
              <div className="qo-card">
                <div className="qo-label">2016 Qualifying Offer</div>
                <div className="qo-amount">{formatCurrencyDetailed(data.qualifying_offer)}</div>
                <div className="qo-description">
                  Average of top 125 MLB salaries
                </div>
              </div>

              {/* Stats Grid */}
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-label">Highest Salary</div>
                  <div className="stat-value">{formatCurrency(data.highest_salary.salary)}</div>
                  <div className="stat-player">{data.highest_salary.player}</div>
                </div>

                <div className="stat-card">
                  <div className="stat-label">125th Salary (Cutoff)</div>
                  <div className="stat-value">{formatCurrency(data.cutoff_salary.salary)}</div>
                  <div className="stat-player">{data.cutoff_salary.player}</div>
                </div>

                <div className="stat-card">
                  <div className="stat-label">Median Salary</div>
                  <div className="stat-value">{formatCurrency(data.median_salary)}</div>
                  <div className="stat-player">Middle of top 125</div>
                </div>

                <div className="stat-card">
                  <div className="stat-label">💰 Salary Gap</div>
                  <div className="stat-value">{formatCurrency(data.salary_spread)}</div>
                  <div className="stat-player">From #1 to #125</div>
                </div>

                <div className="stat-card">
                  <div className="stat-label">Valid Salaries</div>
                  <div className="stat-value">{data.valid_salaries}</div>
                  <div className="stat-player">Players processed</div>
                </div>

                <div className="stat-card">
                  <div className="stat-label">Invalid Entries</div>
                  <div className="stat-value">{data.invalid_salaries}</div>
                  <div className="stat-player">Removed from calculation</div>
                </div>
              </div>

              {/* Percentile Calculator */}
              <div className="calculator-card">
                <h2 className="calculator-title">
                  <span className="calculator-icon">🎯</span>
                  Where Would You Rank?
                </h2>
                <p className="calculator-description">
                  Enter a salary to see where it would rank among the top 125 MLB players
                </p>
                <div className="calculator-input-group">
                  <span className="input-prefix">$</span>
                  <input
                    type="text"
                    className="calculator-input"
                    placeholder="Enter salary (e.g., 15000000)"
                    value={userSalary}
                    onChange={(e) => {
                      const value = e.target.value.replace(/[^0-9]/g, '');
                      setUserSalary(value);
                    }}
                  />
                  <button 
                    className="calculator-button"
                    onClick={() => {
                      const result = handleSalaryCheck();
                      if (result) {
                        const resultEl = document.getElementById('calculator-result');
                        if (resultEl) {
                          resultEl.style.display = 'block';
                        }
                      }
                    }}
                  >
                    Calculate
                  </button>
                </div>
                {userSalary && handleSalaryCheck() && (
                  <div id="calculator-result" className="calculator-result">
                    <div className="result-main">
                      Rank: <strong>#{handleSalaryCheck()!.rank}</strong> of 125
                    </div>
                    <div className="result-sub">
                      {handleSalaryCheck()!.percentile.toFixed(1)}th percentile
                    </div>
                  </div>
                )}
              </div>

              {/* Salary Distribution Chart - Generated by Python/Plotly */}
              <div className="chart-container">
                <h2 className="table-title">
                  <span className="trophy-icon">📊</span>
                  Salary Distribution (Python + Plotly)
                </h2>
                <Plot
                  data={data.chart.data}
                  layout={data.chart.layout}
                  config={{ responsive: true, displayModeBar: false }}
                  style={{ width: '100%', height: '500px' }}
                />
              </div>

              {/* Pie Chart */}
              <div className="chart-container">
                <Plot
                  data={data.pie_chart.data}
                  layout={data.pie_chart.layout}
                  config={{ responsive: true, displayModeBar: false }}
                  style={{ width: '100%', height: '400px' }}
                />
              </div>

              {/* Top 25 Players Table */}
              <div className="table-card">
                <div className="table-header">
                  <h2 className="table-title">
                    <span className="trophy-icon">🏆</span>
                    {showAll ? 'All 125 Players' : 'Top 25 Highest Paid Players'}
                  </h2>
                  <button 
                    className="expand-button"
                    onClick={() => setShowAll(!showAll)}
                  >
                    {showAll ? '📋 Show Top 25' : '📊 Show All 125'}
                  </button>
                </div>
                <div className="table-wrapper">
                  <table className="players-table">
                    <thead>
                      <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Salary</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.top_125.slice(0, showAll ? 125 : 25).map((player, index) => (
                        <tr key={index}>
                          <td className="rank-cell">
                            <span className="rank-badge">{index + 1}</span>
                          </td>
                          <td className="player-cell">{player.player}</td>
                          <td className="salary-cell">{formatCurrency(player.salary)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Note */}
              <div className="note-card">
                <p>
                  <strong>Note:</strong> Data refreshes with each page load. 
                  The qualifying offer is calculated as the average of the top 125 MLB player salaries 
                  from the 2016 season.
                </p>
              </div>
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Built for the Philadelphia Phillies Baseball R&D Team</p>
      </footer>
    </div>
  );
}

export default App;
