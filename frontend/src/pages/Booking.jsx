import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import axios from "axios";

function Booking() {
  const { hostelId } = useParams();
  const navigate = useNavigate();

  const [hostel, setHostel] = useState(null);
  const [loadingHostel, setLoadingHostel] = useState(true);

  const [formData, setFormData] = useState({
    applicant_name: "",
    applicant_phone: "",
    room_type: "",
    move_in_date: "",
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [booking, setBooking] = useState(null);

  useEffect(() => {
    const fetchHostel = async () => {
      try {
        setLoadingHostel(true);

        const response = await axios.get(
          `http://127.0.0.1:5000/api/hostels/${hostelId}`
        );

        const hostelData = response.data.hostel;

        setHostel(hostelData);

        setFormData((previous) => ({
          ...previous,
          room_type: hostelData.room_type,
        }));
      } catch (requestError) {
        console.error(requestError);

        setError(
          requestError.response?.data?.message ||
            "Unable to load hostel information."
        );
      } finally {
        setLoadingHostel(false);
      }
    };

    fetchHostel();
  }, [hostelId]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!formData.applicant_name.trim()) {
      setError("Please enter your full name.");
      return;
    }

    if (!formData.applicant_phone.trim()) {
      setError("Please enter your phone number.");
      return;
    }

    if (!formData.move_in_date) {
      setError("Please select your move-in date.");
      return;
    }

    try {
      setSubmitting(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/api/bookings",
        {
          hostel_id: Number(hostelId),
          applicant_name: formData.applicant_name,
          applicant_phone: formData.applicant_phone,
          room_type: formData.room_type,
          move_in_date: formData.move_in_date,
        }
      );

      setBooking(response.data);
    } catch (requestError) {
      console.error(requestError);

      setError(
        requestError.response?.data?.message ||
          "Unable to submit booking request."
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (loadingHostel) {
    return (
      <div className="booking-page">
        <div className="booking-state">
          <div className="loading-spinner"></div>
          <p>Loading booking information...</p>
        </div>
      </div>
    );
  }

  if (!hostel) {
    return (
      <div className="booking-page">
        <div className="booking-state">
          <div>⚠️</div>

          <h2>
            Hostel Not Found
          </h2>

          <p>
            {error || "Unable to find this hostel."}
          </p>

          <Link
            to="/search"
            className="primary-button"
          >
            Back to Search
          </Link>
        </div>
      </div>
    );
  }

  /* Success */
  if (booking) {
    return (
      <div className="booking-page">

        <nav className="navbar">
          <div className="navbar-container">

            <Link to="/" className="logo">
              Hostel<span>Hub</span>
            </Link>

            <div className="nav-links">
              <Link to="/">
                Home
              </Link>

              <Link to="/search">
                New search
              </Link>

              <Link to="/owner/dashboard">
                Owner Dashboard
              </Link>
            </div>

          </div>
        </nav>

        <main className="booking-success-container">

          <div className="booking-success-card">

            <div className="success-icon">
              ✓
            </div>

            <span className="success-label">
              BOOKING REQUEST SUBMITTED
            </span>

            <h1>
              Your Request is Pending
            </h1>

            <p>
              Your booking request has been successfully
              submitted. The hostel owner will review
              your request.
            </p>

            <div className="booking-id-box">

              <span>
                Booking ID
              </span>

              <strong>
                #{booking.booking_id}
              </strong>

            </div>

            <div className="pending-status">
              <span className="pending-dot"></span>

              Pending Owner Approval
            </div>

            <div className="success-hostel-summary">

              <div>
                <small>
                  Hostel
                </small>

                <strong>
                  {hostel.name}
                </strong>
              </div>

              <div>
                <small>
                  Location
                </small>

                <strong>
                  {hostel.location}
                </strong>
              </div>

              <div>
                <small>
                  Monthly Rent
                </small>

                <strong>
                  Rs. {hostel.rent}
                </strong>
              </div>

            </div>

            <div className="success-actions">

              <Link
                to="/my-bookings"
                className="primary-button"
              >
                View My Bookings
              </Link>

              <Link
                to="/search"
                className="secondary-button"
              >
                Find Another Hostel
              </Link>

            </div>

          </div>

        </main>

      </div>
    );
  }

  return (
    <div className="booking-page">

      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-container">

          <Link to="/" className="logo">
            Chitral<span>Hostel</span>
          </Link>

          <div className="nav-links">
            <Link to="/">
              Home
            </Link>

            <Link to="/search">
              Find Hostel
            </Link>

            <Link to="/owner/dashboard">
              Owner Dashboard
            </Link>
          </div>

        </div>
      </nav>

      {/* Breadcrumb */}
      <div className="details-breadcrumb">
        <div>

          <Link to="/">
            Home
          </Link>

          <span>/</span>

          <Link to={`/hostels/${hostel.id}`}>
            {hostel.name}
          </Link>

          <span>/</span>

          <strong>
            Booking
          </strong>

        </div>
      </div>

      <main className="booking-container">

        {/* Heading */}
        <div className="booking-heading">

          <span>
            BOOKING REQUEST
          </span>

          <h1>
            Request Your Hostel Room
          </h1>

          <p>
            Fill in your information below to send
            a booking request to the hostel owner.
          </p>

        </div>

        <div className="booking-layout">

          {/* Form */}
          <section className="booking-form-card">

            <div className="booking-form-heading">

              <div className="booking-form-number">
                01
              </div>

              <div>
                <h2>
                  Applicant Information
                </h2>

                <p>
                  Enter your contact details.
                </p>
              </div>

            </div>

            <form onSubmit={handleSubmit}>

              <div className="booking-field">

                <label htmlFor="applicant_name">
                  Full Name
                </label>

                <input
                  id="applicant_name"
                  type="text"
                  name="applicant_name"
                  placeholder="Enter your full name"
                  value={formData.applicant_name}
                  onChange={handleChange}
                />

              </div>

              <div className="booking-field">

                <label htmlFor="applicant_phone">
                  Phone Number
                </label>

                <input
                  id="applicant_phone"
                  type="tel"
                  name="applicant_phone"
                  placeholder="03XX XXXXXXX"
                  value={formData.applicant_phone}
                  onChange={handleChange}
                />

              </div>

              <div className="booking-form-heading second">

                <div className="booking-form-number">
                  02
                </div>

                <div>
                  <h2>
                    Room & Move-in Details
                  </h2>

                  <p>
                    Select your preferred move-in date.
                  </p>
                </div>

              </div>

              <div className="booking-field">

                <label htmlFor="room_type">
                  Room Type
                </label>

                <select
                  id="room_type"
                  name="room_type"
                  value={formData.room_type}
                  onChange={handleChange}
                >
                  <option value="Shared">
                    Shared
                  </option>

                  <option value="Single">
                    Single
                  </option>
                </select>

              </div>

              <div className="booking-field">

                <label htmlFor="move_in_date">
                  Move-in Date
                </label>

                <input
                  id="move_in_date"
                  type="date"
                  name="move_in_date"
                  value={formData.move_in_date}
                  onChange={handleChange}
                />

              </div>

              {error && (
                <div className="booking-error">
                  ⚠️ {error}
                </div>
              )}

              <button
                type="submit"
                className="submit-booking-button"
                disabled={submitting}
              >
                {submitting
                  ? "Submitting Request..."
                  : "Submit Booking Request →"}
              </button>

              <p className="booking-form-note">
                Your request will remain Pending until
                the hostel owner accepts or rejects it.
              </p>

            </form>

          </section>

          {/* Summary */}
          <aside className="booking-summary">

            <span className="booking-summary-label">
              SELECTED HOSTEL
            </span>

            <h2>
              {hostel.name}
            </h2>

            <div className="booking-summary-location">
              📍 {hostel.location}
            </div>

            <div className="booking-summary-price">
              <span>
                Monthly Rent
              </span>

              <strong>
                Rs. {hostel.rent}
              </strong>
            </div>

            <div className="booking-summary-info">

              <div>
                <span>
                  Room
                </span>

                <strong>
                  {hostel.room_type}
                </strong>
              </div>

              <div>
                <span>
                  Available
                </span>

                <strong>
                  {hostel.available_rooms}
                </strong>
              </div>

            </div>

            <div className="booking-summary-divider"></div>

            <h3>
              Facilities
            </h3>

            <div className="booking-summary-facilities">

              {hostel.facilities
                ?.split(",")
                .map((facility) => (
                  <span key={facility}>
                    ✓ {facility.trim()}
                  </span>
                ))}

            </div>

            <Link
              to={`/hostels/${hostel.id}`}
              className="back-details-link"
            >
              ← Back to Hostel Details
            </Link>

          </aside>

        </div>

      </main>

    </div>
  );
}

export default Booking;