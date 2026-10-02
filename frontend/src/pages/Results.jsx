import { Link, useLocation, useNavigate } from "react-router-dom";

function Results() {
  const location = useLocation();
  const navigate = useNavigate();

  const recommendations = location.state?.recommendations || [];
  const preferences = location.state?.preferences || {};

  const getScoreClass = (score) => {
    if (score >= 85) return "score-high";
    if (score >= 70) return "score-medium";
    return "score-low";
  };

  const getRecommendationLevelClass = (level) => {
    if (level === "Excellent Match") {
      return "level-excellent";
    }

    if (level === "Good Match") {
      return "level-good";
    }

    if (level === "Moderate Match") {
      return "level-moderate";
    }

    return "level-low";
  };

  const getFacilityList = (facilities) => {
    if (!facilities) {
      return [];
    }

    if (Array.isArray(facilities)) {
      return facilities;
    }

    return facilities
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
  };

  return (
    <div className="results-page">
      <nav className="navbar-container">
        <div className="logo" onClick={() => navigate("/")}>
          Hostel<span>Hub</span>
        </div>

        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/search">New Search</Link>
          <Link to="/my-bookings">My Bookings</Link>
          <Link to="/owner/dashboard">Dashboard</Link>
        </div>
      </nav>

      <section className="results-header">
        <div>
          <span className="results-eyebrow">AI-POWERED SEARCH</span>

          <h1>Recommended Hostels</h1>

          <p>
            Our trained recommendation model ranked these hostels according to
            your preferences.
          </p>
        </div>

        <button
          className="edit-search-button"
          onClick={() => navigate("/search")}
        >
          Edit Search
        </button>
      </section>

      <section className="preference-summary">
        <div className="preference-item">
          <span>Location</span>
          <strong>{preferences.location || "Any"}</strong>
        </div>

        <div className="preference-item">
          <span>Budget</span>
          <strong>Rs. {preferences.budget || "Any"}</strong>
        </div>

        <div className="preference-item">
          <span>Room Type</span>
          <strong>{preferences.room_type || "Any"}</strong>
        </div>

        <div className="preference-item">
          <span>Facilities</span>
          <strong>
            {preferences.facilities?.length
              ? preferences.facilities.join(", ")
              : "Any"}
          </strong>
        </div>
      </section>

      {recommendations.length > 0 ? (
        <section className="results-section">
          <div className="results-section-heading">
            <div>
              <h2>{recommendations.length} Hostels Found</h2>
              <p>Ranked according to your preferences</p>
            </div>
          </div>

          <div className="results-grid">
            {recommendations.map((hostel) => {
              const score = Number(hostel.match_score || 0);
              const facilities = getFacilityList(hostel.facilities);
              const breakdown = hostel.score_breakdown || {};
              const reasons = hostel.why_recommended || [];

              return (
                <article className="result-card" key={hostel.id}>
                  <div className="result-card-top">
                    <div className="rank-badge">#{hostel.rank}</div>

                    <div className="ml-badge">AI/ML Match</div>
                  </div>

                  <div className="match-score-section">
                    <div className={`match-score ${getScoreClass(score)}`}>
                      {score.toFixed(1)}%
                    </div>

                    <div
                      className={`recommendation-level ${getRecommendationLevelClass(
                        hostel.recommendation_level,
                      )}`}
                    >
                      {hostel.recommendation_level}
                    </div>
                  </div>

                  <div className="hostel-main-info">
                    <h3>{hostel.name}</h3>

                    <p className="hostel-location">📍 {hostel.location}</p>
                  </div>

                  <div className="result-details-grid">
                    <div className="result-detail">
                      <span>Monthly Rent</span>
                      <strong>Rs. {hostel.rent}</strong>
                    </div>

                    <div className="result-detail">
                      <span>Room Type</span>
                      <strong>{hostel.room_type}</strong>
                    </div>

                    <div className="result-detail">
                      <span>Available Rooms</span>
                      <strong>{hostel.available_rooms}</strong>
                    </div>
                  </div>

                  <div className="result-facilities">
                    <h4>Facilities</h4>

                    <div className="facility-tags">
                      {facilities.map((facility, index) => (
                        <span key={index} className="facility-tag">
                          {facility}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="why-recommended">
                    <h4>Why this hostel?</h4>

                    <ul>
                      {reasons.map((reason, index) => (
                        <li key={index}>
                          <span className="check-icon">✓</span>

                          {reason}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="score-breakdown">
                    <h4>Match Breakdown</h4>

                    <div className="breakdown-list">
                      <div className="breakdown-row">
                        <span>Budget</span>
                        <strong>{breakdown.budget ?? 0}%</strong>
                      </div>

                      <div className="breakdown-progress">
                        <div
                          style={{
                            width: `${breakdown.budget ?? 0}%`,
                          }}
                        />
                      </div>

                      <div className="breakdown-row">
                        <span>Location</span>
                        <strong>{breakdown.location ?? 0}%</strong>
                      </div>

                      <div className="breakdown-progress">
                        <div
                          style={{
                            width: `${breakdown.location ?? 0}%`,
                          }}
                        />
                      </div>

                      <div className="breakdown-row">
                        <span>Facilities</span>
                        <strong>{breakdown.facilities ?? 0}%</strong>
                      </div>

                      <div className="breakdown-progress">
                        <div
                          style={{
                            width: `${breakdown.facilities ?? 0}%`,
                          }}
                        />
                      </div>

                      <div className="breakdown-row">
                        <span>Room Type</span>
                        <strong>{breakdown.room_type ?? 0}%</strong>
                      </div>

                      <div className="breakdown-progress">
                        <div
                          style={{
                            width: `${breakdown.room_type ?? 0}%`,
                          }}
                        />
                      </div>

                      <div className="breakdown-row">
                        <span>Availability</span>
                        <strong>{breakdown.availability ?? 0}%</strong>
                      </div>

                      <div className="breakdown-progress">
                        <div
                          style={{
                            width: `${breakdown.availability ?? 0}%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>

                  <button
                    className="view-hostel-button"
                    onClick={() => navigate(`/hostels/${hostel.id}`)}
                  >
                    View Hostel Details <span>→</span>
                  </button>
                </article>
              );
            })}
          </div>
        </section>
      ) : (
        <section className="no-results">
          <div className="no-results-icon">🔍</div>

          <h2>No Hostels Found</h2>

          <p>
            Try changing your budget, location, room type, or facility
            preferences.
          </p>

          <button onClick={() => navigate("/search")}>
            Try Another Search
          </button>
        </section>
      )}
    </div>
  );
}

export default Results;
