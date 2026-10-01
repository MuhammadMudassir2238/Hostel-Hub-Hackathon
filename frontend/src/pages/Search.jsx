import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function Search() {
  const navigate = useNavigate();

  const [preferences, setPreferences] = useState({
    location: "Chitral Town",
    budget: "",
    room_type: "Shared",
    facilities: [],
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const facilitiesList = [
    "WiFi",
    "Mess",
    "Heating",
    "Attached Bathroom",
  ];

  const handleChange = (event) => {
    const { name, value } = event.target;

    setPreferences((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleFacilityChange = (facility) => {
    setPreferences((previous) => {
      const alreadySelected =
        previous.facilities.includes(facility);

      return {
        ...previous,
        facilities: alreadySelected
          ? previous.facilities.filter(
              (item) => item !== facility
            )
          : [...previous.facilities, facility],
      };
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!preferences.budget) {
      setError("Please enter your monthly budget.");
      return;
    }

    if (Number(preferences.budget) <= 0) {
      setError("Budget must be greater than 0.");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/api/recommend",
        {
          budget: Number(preferences.budget),
          location: preferences.location,
          room_type: preferences.room_type,
          facilities: preferences.facilities,
        }
      );

      navigate("/results", {
        state: {
          recommendations:
            response.data.recommendations,
          preferences,
        },
      });
    } catch (requestError) {
      console.error(requestError);

      setError(
        requestError.response?.data?.message ||
          "Unable to get recommendations. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">

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
              Owner Dashboard
            </Link>
          </div>

        </div>
      </nav>

      {/* Search Header */}
      <section className="search-header">

        <div className="search-header-content">

          <span className="search-badge">
            🤖 AI HOSTEL FINDER
          </span>

          <h1>
            Tell Us What You Need
          </h1>

          <p>
            Enter your preferences and our recommendation
            engine will find hostels that match your
            requirements.
          </p>

        </div>

      </section>

      {/* Search Form */}
      <main className="search-container">

        <form
          className="search-form"
          onSubmit={handleSubmit}
        >

          {/* Location */}
          <div className="form-section">

            <div className="form-section-heading">
              <span className="form-number">01</span>

              <div>
                <h2>Preferred Location</h2>
                <p>
                  Where do you want to stay?
                </p>
              </div>
            </div>

            <label htmlFor="location">
              Location
            </label>

            <select
              id="location"
              name="location"
              value={preferences.location}
              onChange={handleChange}
            >
              <option value="Chitral Town">
                Chitral Town
              </option>

              <option value="Drosh">
                Drosh
              </option>

              <option value="Booni">
                Booni
              </option>

              <option value="Chitral">
                Chitral
              </option>
            </select>

          </div>

          {/* Budget */}
          <div className="form-section">

            <div className="form-section-heading">
              <span className="form-number">02</span>

              <div>
                <h2>Monthly Budget</h2>
                <p>
                  How much can you spend per month?
                </p>
              </div>
            </div>

            <label htmlFor="budget">
              Maximum Monthly Budget
            </label>

            <div className="budget-input">

              <span>Rs.</span>

              <input
                id="budget"
                type="number"
                name="budget"
                min="1"
                placeholder="e.g. 10000"
                value={preferences.budget}
                onChange={handleChange}
              />

              <span>/ month</span>

            </div>

          </div>

          {/* Room Type */}
          <div className="form-section">

            <div className="form-section-heading">
              <span className="form-number">03</span>

              <div>
                <h2>Room Type</h2>
                <p>
                  Select your preferred room arrangement.
                </p>
              </div>
            </div>

            <div className="room-options">

              <label
                className={
                  preferences.room_type === "Shared"
                    ? "room-option selected"
                    : "room-option"
                }
              >
                <input
                  type="radio"
                  name="room_type"
                  value="Shared"
                  checked={
                    preferences.room_type === "Shared"
                  }
                  onChange={handleChange}
                />

                <span className="room-icon">
                  👥
                </span>

                <span>
                  <strong>Shared</strong>
                  <small>
                    Shared room
                  </small>
                </span>
              </label>

              <label
                className={
                  preferences.room_type === "Single"
                    ? "room-option selected"
                    : "room-option"
                }
              >
                <input
                  type="radio"
                  name="room_type"
                  value="Single"
                  checked={
                    preferences.room_type === "Single"
                  }
                  onChange={handleChange}
                />

                <span className="room-icon">
                  👤
                </span>

                <span>
                  <strong>Single</strong>
                  <small>
                    Private room
                  </small>
                </span>
              </label>

            </div>

          </div>

          {/* Facilities */}
          <div className="form-section">

            <div className="form-section-heading">
              <span className="form-number">04</span>

              <div>
                <h2>Required Facilities</h2>
                <p>
                  Select facilities that matter to you.
                </p>
              </div>
            </div>

            <div className="facility-options">

              {facilitiesList.map((facility) => {

                const selected =
                  preferences.facilities.includes(
                    facility
                  );

                return (
                  <label
                    key={facility}
                    className={
                      selected
                        ? "facility-option selected"
                        : "facility-option"
                    }
                  >

                    <input
                      type="checkbox"
                      checked={selected}
                      onChange={() =>
                        handleFacilityChange(
                          facility
                        )
                      }
                    />

                    <span className="facility-check">
                      {selected ? "✓" : ""}
                    </span>

                    <span>
                      {facility}
                    </span>

                  </label>
                );
              })}

            </div>

          </div>

          {/* Error */}
          {error && (
            <div className="search-error">
              ⚠️ {error}
            </div>
          )}

          {/* Submit */}
          <div className="search-submit">

            <div>
              <strong>
                Ready to find your hostel?
              </strong>

              <p>
                Our AI recommendation engine will
                compare available hostels for you.
              </p>
            </div>

            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Finding Hostels..."
                : "Find My Hostel →"}
            </button>

          </div>

        </form>

      </main>

    </div>
  );
}

export default Search;