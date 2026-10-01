import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function OwnerDashboard() {
  const navigate = useNavigate();

  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ==========================================
  // LOAD ALL BOOKINGS
  // ==========================================

  const loadBookings = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await axios.get("http://127.0.0.1:5000/api/bookings");

      setBookings(response.data.bookings || []);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.message || "Failed to load booking requests.",
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // LOAD DATA WHEN PAGE OPENS
  // ==========================================

  useEffect(() => {
    loadBookings();
  }, []);

  // ==========================================
  // REFRESH DASHBOARD
  // ==========================================

  const refreshDashboard = () => {
    loadBookings();
  };

  // ==========================================
  // UPDATE BOOKING STATUS
  // ==========================================

  const updateStatus = async (bookingId, status) => {
    try {
      const response = await axios.put(
        `http://127.0.0.1:5000/api/bookings/${bookingId}/status`,
        {
          status: status,
        },
      );

      if (response.data.success) {
        setBookings((currentBookings) =>
          currentBookings.map((booking) =>
            booking.id === bookingId
              ? {
                  ...booking,
                  status: status,
                }
              : booking,
          ),
        );
      }
    } catch (err) {
      console.error(err);

      alert(err.response?.data?.message || "Failed to update booking status.");
    }
  };

  // ==========================================
  // STATUS CSS CLASS
  // ==========================================

  const getStatusClass = (status) => {
    if (status === "Accepted") {
      return "status-accepted";
    }

    if (status === "Rejected") {
      return "status-rejected";
    }

    return "status-pending";
  };

  // ==========================================
  // DASHBOARD STATISTICS
  // ==========================================

  const totalBookings = bookings.length;

  const pendingBookings = bookings.filter(
    (booking) => booking.status === "Pending",
  ).length;

  const acceptedBookings = bookings.filter(
    (booking) => booking.status === "Accepted",
  ).length;

  const rejectedBookings = bookings.filter(
    (booking) => booking.status === "Rejected",
  ).length;

  // ==========================================
  // UI
  // ==========================================

  return (
    <div className="owner-dashboard-page">
      {/* =====================================
          NAVBAR
      ===================================== */}

      <nav className="dashboard-navbar">
        <div className="dashboard-logo" onClick={() => navigate("/")}>
          ChitralHostel
        </div>

        <div className="dashboard-nav-links">
          <button onClick={() => navigate("/")}>Home</button>

          <button onClick={() => navigate("/owner/listings")}>
            Manage Listings
          </button>

          <button onClick={() => navigate("/search")}>Find Hostel</button>
        </div>
      </nav>

      {/* =====================================
          MAIN CONTENT
      ===================================== */}

      <main className="dashboard-container">
        {/* ===================================
            HEADER
        =================================== */}

        <div className="dashboard-header">
          <div>
            <p className="dashboard-eyebrow">OWNER PANEL</p>

            <h1>Owner Dashboard</h1>

            <p>Manage booking requests and monitor your hostel reservations.</p>
          </div>

          <div className="dashboard-header-actions">
            <button
              className="manage-listings-button"
              onClick={() => navigate("/owner/listings")}
            >
              Manage Listings
            </button>

            <button className="refresh-button" onClick={refreshDashboard}>
              Refresh
            </button>
          </div>
        </div>

        {/* ===================================
            ERROR MESSAGE
        =================================== */}

        {error && <div className="dashboard-error">{error}</div>}

        {/* ===================================
            STATISTICS
        =================================== */}

        <section className="dashboard-stats">
          <div className="stat-card">
            <div className="stat-icon">📋</div>

            <div>
              <span>Total Requests</span>

              <strong>{totalBookings}</strong>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⏳</div>

            <div>
              <span>Pending</span>

              <strong>{pendingBookings}</strong>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">✓</div>

            <div>
              <span>Accepted</span>

              <strong>{acceptedBookings}</strong>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">✕</div>

            <div>
              <span>Rejected</span>

              <strong>{rejectedBookings}</strong>
            </div>
          </div>
        </section>

        {/* ===================================
            BOOKING REQUESTS
        =================================== */}

        <section className="dashboard-section">
          <div className="section-heading">
            <div>
              <p className="section-eyebrow">RESERVATIONS</p>

              <h2>Booking Requests</h2>

              <p>
                Review and manage booking requests submitted by hostel
                applicants.
              </p>
            </div>
          </div>

          {/* =================================
              LOADING
          ================================= */}

          {loading && (
            <div className="dashboard-loading">
              <div className="loading-spinner"></div>

              <p>Loading booking requests...</p>
            </div>
          )}

          {/* =================================
              EMPTY STATE
          ================================= */}

          {!loading && bookings.length === 0 && (
            <div className="dashboard-empty">
              <div className="empty-icon">📭</div>

              <h3>No Booking Requests</h3>

              <p>No booking requests have been submitted yet.</p>
            </div>
          )}

          {/* =================================
              BOOKING LIST
          ================================= */}

          {!loading && bookings.length > 0 && (
            <div className="booking-request-list">
              {bookings.map((booking) => (
                <div className="booking-request-card" key={booking.id}>
                  {/* =========================
                      CARD HEADER
                  ========================= */}

                  <div className="booking-card-header">
                    <div>
                      <span className="booking-id">Booking #{booking.id}</span>

                      <h3>{booking.hostel_name}</h3>

                      <p className="booking-location">
                        📍 {booking.hostel_location}
                      </p>
                    </div>

                    <span
                      className={`booking-status ${getStatusClass(
                        booking.status,
                      )}`}
                    >
                      {booking.status}
                    </span>
                  </div>

                  {/* =========================
                      BOOKING INFORMATION
                  ========================= */}

                  <div className="booking-information">
                    <div className="booking-info-item">
                      <span>Applicant</span>

                      <strong>{booking.applicant_name}</strong>
                    </div>

                    <div className="booking-info-item">
                      <span>Phone</span>

                      <strong>{booking.applicant_phone}</strong>
                    </div>

                    <div className="booking-info-item">
                      <span>Room Type</span>

                      <strong>{booking.room_type}</strong>
                    </div>

                    <div className="booking-info-item">
                      <span>Move-in Date</span>

                      <strong>{booking.move_in_date}</strong>
                    </div>

                    <div className="booking-info-item">
                      <span>Monthly Rent</span>

                      <strong>Rs. {booking.hostel_rent}</strong>
                    </div>
                  </div>

                  {/* =========================
                      ACTIONS
                  ========================= */}

                  <div className="booking-card-actions">
                    {booking.status === "Pending" ? (
                      <>
                        <button
                          className="accept-button"
                          onClick={() => updateStatus(booking.id, "Accepted")}
                        >
                          Accept
                        </button>

                        <button
                          className="reject-button"
                          onClick={() => updateStatus(booking.id, "Rejected")}
                        >
                          Reject
                        </button>
                      </>
                    ) : (
                      <div className="status-message">
                        {booking.status === "Accepted" && (
                          <span>✓ Booking accepted successfully.</span>
                        )}

                        {booking.status === "Rejected" && (
                          <span>Booking request rejected.</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default OwnerDashboard;
