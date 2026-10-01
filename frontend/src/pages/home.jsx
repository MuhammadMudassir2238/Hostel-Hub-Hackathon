import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-page">

      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-container">

          <Link to="/" className="logo">
            Hostel<span>Hub</span>
          </Link>

          <div className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/my-bookings">My Bookings</Link>
            <Link to="/owner/dashboard">
              Dashboard
            </Link>
          </div>

        </div>
      </nav>

      {/* Hero */}
      <section className="hero-section">

        <div className="hero-content">

          <div className="hero-text">

            <div className="hero-badge">
              AI-Powered Hostel Finder
            </div>

            <h1>
              Find the Right
              <span> Hostel in Chitral</span>
            </h1>

            <p>
              Discover hostels based on your budget,
              preferred location, room type and facilities
              using our smart recommendation system.
            </p>

            <div className="hero-buttons">

              <Link
                to="/search"
                className="primary-button"
              >
                Find Your Hostel
              </Link>

              <Link
                to="/owner/dashboard"
                className="secondary-button"
              >
                Owner Dashboard
              </Link>

            </div>

          </div>

          <div className="hero-card">

            <div className="hero-card-icon">
              🏠
            </div>

            <h3>Smart Hostel Matching</h3>

            <p>
              Our recommendation engine compares
              hostels according to your preferences.
            </p>

            <div className="hero-score">
              <strong>AI Match</strong>
              <span>100%</span>
            </div>

          </div>

        </div>

      </section>

      {/* Features */}
      <section className="features-section">

        <div className="section-header">

          <span>WHY CHOOSE US</span>

          <h2>
            Everything You Need to Find a Hostel
          </h2>

          <p>
            A simple digital solution for students
            and residents looking for accommodation
            in Chitral.
          </p>

        </div>

        <div className="features-grid">

          <div className="feature-card">

            <div className="feature-icon">
              🤖
            </div>

            <h3>AI Recommendations</h3>

            <p>
              Get hostel recommendations based on
              your budget, location, facilities and
              preferred room type.
            </p>

          </div>

          <div className="feature-card">

            <div className="feature-icon">
              📍
            </div>

            <h3>Location & Map</h3>

            <p>
              Explore hostel locations on an
              interactive map and understand where
              each hostel is located.
            </p>

          </div>

          <div className="feature-card">

            <div className="feature-icon">
              📋
            </div>

            <h3>Easy Booking</h3>

            <p>
              Submit a booking request online and
              track whether your request is pending,
              accepted or rejected.
            </p>

          </div>

        </div>

      </section>

      {/* How It Works */}
      <section className="how-section">

        <div className="section-header">

          <span>HOW IT WORKS</span>

          <h2>
            Find Your Hostel in 3 Simple Steps
          </h2>

        </div>

        <div className="steps-grid">

          <div className="step-card">

            <div className="step-number">
              01
            </div>

            <h3>Set Preferences</h3>

            <p>
              Enter your budget, location,
              room type and required facilities.
            </p>

          </div>

          <div className="step-card">

            <div className="step-number">
              02
            </div>

            <h3>Get Recommendations</h3>

            <p>
              The recommendation engine calculates
              a match score for available hostels.
            </p>

          </div>

          <div className="step-card">

            <div className="step-number">
              03
            </div>

            <h3>Book Your Hostel</h3>

            <p>
              View hostel details and submit your
              booking request directly online.
            </p>

          </div>

        </div>

      </section>

      {/* CTA */}
      <section className="cta-section">

        <div>

          <h2>
            Ready to Find Your Hostel?
          </h2>

          <p>
            Start searching and discover accommodation
            that matches your requirements.
          </p>

        </div>

        <Link
          to="/search"
          className="cta-button"
        >
          Start Searching
        </Link>

      </section>

      {/* Footer */}
      <footer className="footer">

        <div>
          <strong>ChitralHostel</strong>

          <p>
            AI-powered hostel discovery and booking
            platform for Chitral.
          </p>
        </div>

        <div className="footer-right">
          Hackathon Prototype
        </div>

      </footer>

    </div>
  );
}

export default Home;