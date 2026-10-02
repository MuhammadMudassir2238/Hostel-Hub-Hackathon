import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function MyBookings() {
  const navigate = useNavigate();

  const [phone, setPhone] = useState("");
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  const searchBookings = async (event) => {
    event.preventDefault();

    if (!phone.trim()) {
      setError("Please enter your phone number.");
      setBookings([]);
      setSearched(false);
      return;
    }

    setLoading(true);
    setError("");
    setSearched(true);

    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/api/my-bookings?phone=${encodeURIComponent(
          phone.trim()
        )}`
      );

      setBookings(response.data.bookings || []);
    } catch (error) {
      console.error(error);

      setBookings([]);

      setError(
        error.response?.data?.message ||
          "Unable to find your bookings."
      );
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (status) => {
    if (status === "Accepted") {
      return "status-accepted";
    }

    if (status === "Rejected") {
      return "status-rejected";
    }

    return "status-pending";
  };

  return (
    <div className="my-bookings-page">
      <nav className="navbar">
        <div className="logo">
          Hostel<span>Hub</span>
        </div>

        <div className="nav-actions">
          <button
            className="nav-button"
            onClick={() => navigate("/")}
          >
            Home
          </button>

          <button
            className="nav-button"
            onClick={() => navigate("/search")}
          >
            Find Hostel
          </button>
        </div>
      </nav>

      <main className="my-bookings-container">
        <section className="my-bookings-header">
          <p className="hero-label">
            MY BOOKINGS
          </p>

          <h1>
            Check Your Booking Status
          </h1>

          <p>
            Enter the phone number used when
            submitting your booking request.
          </p>
        </section>

        <section className="booking-search-card">
          <form
            onSubmit={searchBookings}
            className="booking-search-form"
          >
            <div className="booking-search-input">
              <label htmlFor="booking-phone">
                Phone Number
              </label>

              <input
                id="booking-phone"
                type="tel"
                placeholder="03XXXXXXXXX"
                value={phone}
                onChange={(event) =>
                  setPhone(event.target.value)
                }
              />
            </div>

            <button
              type="submit"
              className="primary-button"
              disabled={loading}
            >
              {loading
                ? "Searching..."
                : "Find My Bookings"}
            </button>
          </form>

          {error && (
            <div className="booking-error">
              {error}
            </div>
          )}
        </section>
        {loading && (
          <div className="my-bookings-loading">
            <div className="loading-spinner"></div>

            <p>
              Searching your booking requests...
            </p>
          </div>
        )}

        {searched &&
          !loading &&
          !error &&
          bookings.length === 0 && (
            <div className="my-bookings-empty">
              <div className="empty-icon">
                📋
              </div>

              <h2>
                No Bookings Found
              </h2>

              <p>
                We could not find any booking
                requests for this phone number.
              </p>

              <button
                className="primary-button"
                onClick={() => navigate("/search")}
              >
                Find a Hostel
              </button>
            </div>
          )}

        {!loading && bookings.length > 0 && (
          <section className="my-bookings-results">
            <div className="results-heading">
              <div>
                <p className="section-label">
                  BOOKING HISTORY
                </p>

                <h2>
                  Your Booking Requests
                </h2>
              </div>

              <span className="booking-count">
                {bookings.length} booking
                {bookings.length !== 1
                  ? "s"
                  : ""}
              </span>
            </div>

            <div className="my-booking-list">
              {bookings.map((booking) => (
                <article
                  className="my-booking-card"
                  key={booking.id}
                >
                  <div className="my-booking-top">
                    <div className="booking-hostel-info">
                      <span className="booking-id">
                        Booking #{booking.id}
                      </span>

                      <h3>
                        {booking.hostel_name}
                      </h3>

                      <p>
                        📍 {booking.hostel_location}
                      </p>
                    </div>

                    <span
                      className={`booking-status ${getStatusClass(
                        booking.status
                      )}`}
                    >
                      <span className="status-dot"></span>
                      {booking.status}
                    </span>
                  </div>

                  <div className="my-booking-details">
                    <div className="booking-detail-item">
                      <span>
                        Applicant
                      </span>

                      <strong>
                        {booking.applicant_name}
                      </strong>
                    </div>

                    <div className="booking-detail-item">
                      <span>
                        Phone
                      </span>

                      <strong>
                        {booking.applicant_phone}
                      </strong>
                    </div>

                    <div className="booking-detail-item">
                      <span>
                        Room Type
                      </span>

                      <strong>
                        {booking.room_type}
                      </strong>
                    </div>

                    <div className="booking-detail-item">
                      <span>
                        Move-in Date
                      </span>

                      <strong>
                        {booking.move_in_date}
                      </strong>
                    </div>

                    <div className="booking-detail-item">
                      <span>
                        Monthly Rent
                      </span>

                      <strong>
                        Rs. {booking.hostel_rent}
                      </strong>
                    </div>
                  </div>

                  {/* Status Message */}
                  <div className="my-booking-footer">
                    <div className="booking-status-message">
                      {booking.status === "Pending" && (
                        <p>
                          Your request is waiting for
                          the hostel owner to review.
                        </p>
                      )}

                      {booking.status === "Accepted" && (
                        <p className="accepted-message">
                          ✓ Your booking request has
                          been accepted by the hostel
                          owner.
                        </p>
                      )}

                      {booking.status === "Rejected" && (
                        <p className="rejected-message">
                          Your booking request was
                          rejected by the hostel owner.
                        </p>
                      )}
                    </div>

                    <button
                      className="secondary-button"
                      onClick={() =>
                        navigate(
                          `/hostels/${booking.hostel_id}`
                        )
                      }
                    >
                      View Hostel
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default MyBookings;

