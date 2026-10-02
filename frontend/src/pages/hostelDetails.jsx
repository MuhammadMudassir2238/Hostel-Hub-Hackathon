import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import axios from "axios";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import L from "leaflet";

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function HostelDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [hostel, setHostel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHostel = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await axios.get(
          `http://127.0.0.1:5000/api/hostels/${id}`
        );

        setHostel(response.data.hostel);
      } catch (requestError) {
        console.error(requestError);

        setError(
          requestError.response?.data?.message ||
            "Unable to load hostel details."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHostel();
  }, [id]);

  if (loading) {
    return (
      <div className="details-page">
        <div className="details-state">
          <div className="loading-spinner"></div>
          <p>Loading hostel details...</p>
        </div>
      </div>
    );
  }

  if (error || !hostel) {
    return (
      <div className="details-page">
        <div className="details-state error-state">
          <div>⚠️</div>

          <h2>
            Unable to Load Hostel
          </h2>

          <p>
            {error || "Hostel not found."}
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

  const facilities = hostel.facilities
    ? hostel.facilities
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean)
    : [];

  const hasLocation =
    hostel.latitude !== null &&
    hostel.latitude !== undefined &&
    hostel.longitude !== null &&
    hostel.longitude !== undefined;

  return (
    <div className="details-page">

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
              New Search
            </Link>
            <Link to="/my-bookings">My Bookings</Link>

            <Link to="/owner/dashboard">
              Owner Dashboard
            </Link>
          </div>

        </div>
      </nav>

      <div className="details-breadcrumb">
        <div>
          <Link to="/">
            Home
          </Link>

          <span>/</span>

          <Link to="/search">
            Search
          </Link>

          <span>/</span>

          <strong>
            {hostel.name}
          </strong>
        </div>
      </div>

      <main className="details-container">

        <section className="details-hero">

          <div className="details-hero-content">

            <span className="details-badge">
              🏠 HOSTEL DETAILS
            </span>

            <h1>
              {hostel.name}
            </h1>

            <div className="details-location">
              📍 {hostel.location}
            </div>

            <p>
              {hostel.description ||
                "Comfortable accommodation with facilities suitable for students and residents in Chitral."}
            </p>

          </div>

          <div className="details-price-card">

            <span>
              Monthly Rent
            </span>

            <strong>
              Rs. {hostel.rent}
            </strong>

            <small>
              per month
            </small>

          </div>

        </section>
        <section className="quick-info-grid">

          <div className="quick-info-card">

            <div className="quick-info-icon">
              🛏️
            </div>

            <div>
              <small>
                Room Type
              </small>

              <strong>
                {hostel.room_type}
              </strong>
            </div>

          </div>

          <div className="quick-info-card">

            <div className="quick-info-icon">
              🟢
            </div>

            <div>
              <small>
                Available Rooms
              </small>

              <strong>
                {hostel.available_rooms}
              </strong>
            </div>

          </div>

          <div className="quick-info-card">

            <div className="quick-info-icon">
              📍
            </div>

            <div>
              <small>
                Location
              </small>

              <strong>
                {hostel.location}
              </strong>
            </div>

          </div>

          <div className="quick-info-card">

            <div className="quick-info-icon">
              💰
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

        </section>
        <div className="details-layout">
          <div className="details-main-column">
            <section className="details-card">

              <div className="details-card-heading">

                <div>
                  <span>
                    AMENITIES
                  </span>

                  <h2>
                    Available Facilities
                  </h2>
                </div>

              </div>

              {facilities.length > 0 ? (
                <div className="details-facilities">

                  {facilities.map(
                    (facility) => (
                      <div
                        className="details-facility"
                        key={facility}
                      >
                        <span>
                          ✓
                        </span>

                        {facility}
                      </div>
                    )
                  )}

                </div>
              ) : (
                <p className="muted-text">
                  No facilities listed.
                </p>
              )}

            </section>
            <section className="details-card">

              <div className="details-card-heading">

                <div>
                  <span>
                    ABOUT
                  </span>

                  <h2>
                    About This Hostel
                  </h2>
                </div>

              </div>

              <p className="description-text">
                {hostel.description ||
                  "No detailed description is currently available for this hostel."}
              </p>

            </section>
            <section className="details-card">

              <div className="details-card-heading">

                <div>
                  <span>
                    LOCATION
                  </span>

                  <h2>
                    Hostel Location
                  </h2>
                </div>

                <span className="map-label">
                  OpenStreetMap
                </span>

              </div>

              {hasLocation ? (
                <div className="hostel-map">

                  <MapContainer
                    center={[
                      Number(hostel.latitude),
                      Number(hostel.longitude),
                    ]}
                    zoom={14}
                    scrollWheelZoom={false}
                    style={{
                      height: "360px",
                      width: "100%",
                    }}
                  >

                    <TileLayer
                      attribution="&copy; OpenStreetMap contributors"
                      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />

                    <Marker
                      position={[
                        Number(hostel.latitude),
                        Number(hostel.longitude),
                      ]}
                    >
                      <Popup>
                        <strong>
                          {hostel.name}
                        </strong>

                        <br />

                        {hostel.location}
                      </Popup>
                    </Marker>

                  </MapContainer>

                </div>
              ) : (
                <div className="map-unavailable">
                  📍 Location coordinates are not
                  available for this hostel.
                </div>
              )}

            </section>

          </div>


          <aside className="details-sidebar">


            <div className="booking-card">

              <span className="booking-label">
                READY TO MOVE?
              </span>

              <h2>
                Book This Hostel
              </h2>

              <p>
                Submit a booking request and wait
                for the owner to approve it.
              </p>

              <div className="booking-availability">

                <span>
                  Available Rooms
                </span>

                <strong
                  className={
                    hostel.available_rooms > 0
                      ? "available"
                      : "unavailable"
                  }
                >
                  {hostel.available_rooms > 0
                    ? `${hostel.available_rooms} Available`
                    : "No Rooms Available"}
                </strong>

              </div>

              <button
                className="booking-button"
                disabled={
                  hostel.available_rooms <= 0
                }
                onClick={() =>
                  navigate(
                    `/booking/${hostel.id}`
                  )
                }
              >
                {hostel.available_rooms > 0
                  ? "Request Booking →"
                  : "Currently Unavailable"}
              </button>

              <small className="booking-note">
                Booking request is subject to owner
                approval.
              </small>

            </div>

            <div className="owner-card">

              <span className="owner-label">
                HOSTEL OWNER
              </span>

              <h3>
                {hostel.owner_name ||
                  "Hostel Owner"}
              </h3>

              {hostel.owner_phone && (
                <div className="owner-contact">
                  📞 {hostel.owner_phone}
                </div>
              )}

              <p>
                Contact information is provided for
                hostel-related communication.
              </p>

            </div>

          </aside>

        </div>

      </main>

    </div>
  );
}

export default HostelDetails;