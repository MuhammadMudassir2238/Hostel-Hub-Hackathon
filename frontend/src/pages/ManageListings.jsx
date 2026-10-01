import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function ManageListings() {
  const navigate = useNavigate();

  const [hostels, setHostels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    location: "",
    rent: "",
    room_type: "",
    facilities: "",
    available_rooms: "",
    description: "",
    owner_name: "",
    owner_phone: "",
  });

  // ==========================================
  // LOAD HOSTELS
  // ==========================================

  const loadHostels = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await axios.get(
        "http://127.0.0.1:5000/api/hostels"
      );

      setHostels(response.data.hostels || []);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.message ||
          "Failed to load hostel listings."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHostels();
  }, []);

  // ==========================================
  // START EDITING
  // ==========================================

  const startEditing = (hostel) => {
    setEditingId(hostel.id);

    setFormData({
      name: hostel.name || "",
      location: hostel.location || "",
      rent: hostel.rent || "",
      room_type: hostel.room_type || "",
      facilities: hostel.facilities || "",
      available_rooms: hostel.available_rooms ?? "",
      description: hostel.description || "",
      owner_name: hostel.owner_name || "",
      owner_phone: hostel.owner_phone || "",
    });

    setSuccess("");
    setError("");
  };

  // ==========================================
  // FORM CHANGE
  // ==========================================

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  // ==========================================
  // UPDATE HOSTEL
  // ==========================================

  const handleUpdate = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    try {
      const response = await axios.put(
        `http://127.0.0.1:5000/api/hostels/${editingId}`,
        {
          name: formData.name,
          location: formData.location,
          rent: Number(formData.rent),
          room_type: formData.room_type,
          facilities: formData.facilities,
          available_rooms: Number(
            formData.available_rooms
          ),
          description: formData.description,
          owner_name: formData.owner_name,
          owner_phone: formData.owner_phone,
        }
      );

      if (response.data.success) {
        setHostels((currentHostels) =>
          currentHostels.map((hostel) =>
            hostel.id === editingId
              ? response.data.hostel
              : hostel
          )
        );

        setSuccess(
          "Hostel listing updated successfully."
        );

        setEditingId(null);
      }
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.message ||
          "Failed to update hostel listing."
      );
    }
  };

  // ==========================================
  // CANCEL EDITING
  // ==========================================

  const cancelEditing = () => {
    setEditingId(null);

    setFormData({
      name: "",
      location: "",
      rent: "",
      room_type: "",
      facilities: "",
      available_rooms: "",
      description: "",
      owner_name: "",
      owner_phone: "",
    });

    setError("");
  };

  // ==========================================
  // UI
  // ==========================================

  return (
    <div className="manage-listings-page">

      {/* ======================================
          NAVBAR
      ====================================== */}

      <nav className="listings-navbar">

        <div
          className="listings-logo"
          onClick={() => navigate("/")}
        >
          ChitralHostel
        </div>

        <div className="listings-nav-links">

          <button
            onClick={() => navigate("/")}
          >
            Home
          </button>

          <button
            onClick={() =>
              navigate("/owner/dashboard")
            }
          >
            Dashboard
          </button>

          <button
            onClick={() => navigate("/search")}
          >
            Find Hostel
          </button>

        </div>

      </nav>

      {/* ======================================
          MAIN
      ====================================== */}

      <main className="listings-container">

        {/* ====================================
            HEADER
        ==================================== */}

        <div className="listings-header">

          <div>

            <p className="listings-eyebrow">
              OWNER PANEL
            </p>

            <h1>
              Manage Listings
            </h1>

            <p>
              View, edit and manage your hostel
              information and room availability.
            </p>

          </div>

          <button
            className="back-dashboard-button"
            onClick={() =>
              navigate("/owner/dashboard")
            }
          >
            ← Dashboard
          </button>

        </div>

        {/* ====================================
            SUCCESS
        ==================================== */}

        {success && (
          <div className="listing-success">
            ✓ {success}
          </div>
        )}

        {/* ====================================
            ERROR
        ==================================== */}

        {error && (
          <div className="listing-error">
            {error}
          </div>
        )}

        {/* ====================================
            LOADING
        ==================================== */}

        {loading && (
          <div className="listings-loading">

            <div className="listing-spinner"></div>

            <p>
              Loading hostel listings...
            </p>

          </div>
        )}

        {/* ====================================
            EMPTY
        ==================================== */}

        {!loading && hostels.length === 0 && (
          <div className="listings-empty">

            <div className="empty-listing-icon">
              🏠
            </div>

            <h2>
              No Hostel Listings
            </h2>

            <p>
              No hostel listings are available.
            </p>

          </div>
        )}

        {/* ====================================
            HOSTEL GRID
        ==================================== */}

        {!loading && hostels.length > 0 && (
          <div className="listings-grid">

            {hostels.map((hostel) => (
              <article
                className="listing-card"
                key={hostel.id}
              >

                {/* CARD TOP */}

                <div className="listing-card-top">

                  <div className="listing-house-icon">
                    🏠
                  </div>

                  <span className="listing-id">
                    ID #{hostel.id}
                  </span>

                </div>

                {/* TITLE */}

                <div className="listing-title-section">

                  <h2>
                    {hostel.name}
                  </h2>

                  <p>
                    📍 {hostel.location}
                  </p>

                </div>

                {/* MAIN INFO */}

                <div className="listing-main-info">

                  <div className="listing-price">

                    <span>
                      Monthly Rent
                    </span>

                    <strong>
                      Rs. {hostel.rent}
                    </strong>

                  </div>

                  <div className="listing-room">

                    <span>
                      Room Type
                    </span>

                    <strong>
                      {hostel.room_type}
                    </strong>

                  </div>

                </div>

                {/* AVAILABILITY */}

                <div className="listing-availability">

                  <div>

                    <span>
                      Available Rooms
                    </span>

                    <strong>
                      {hostel.available_rooms}
                    </strong>

                  </div>

                  <span
                    className={
                      hostel.available_rooms > 0
                        ? "availability-active"
                        : "availability-full"
                    }
                  >
                    {hostel.available_rooms > 0
                      ? "Available"
                      : "Full"}
                  </span>

                </div>

                {/* FACILITIES */}

                <div className="listing-facilities">

                  <span>
                    Facilities
                  </span>

                  <div className="facility-tags">

                    {hostel.facilities
                      ?.split(",")
                      .map((facility, index) => (
                        <span
                          key={index}
                          className="facility-tag"
                        >
                          {facility.trim()}
                        </span>
                      ))}

                  </div>

                </div>

                {/* OWNER */}

                <div className="listing-owner">

                  <span>
                    Owner
                  </span>

                  <strong>
                    {hostel.owner_name ||
                      "Not provided"}
                  </strong>

                  <small>
                    {hostel.owner_phone ||
                      "No phone provided"}
                  </small>

                </div>

                {/* ACTIONS */}

                <div className="listing-actions">

                  <button
                    className="edit-listing-button"
                    onClick={() =>
                      startEditing(hostel)
                    }
                  >
                    Edit Listing
                  </button>

                  <button
                    className="view-listing-button"
                    onClick={() =>
                      navigate(
                        `/hostels/${hostel.id}`
                      )
                    }
                  >
                    View
                  </button>

                </div>

              </article>
            ))}

          </div>
        )}

      </main>

      {/* ======================================
          EDIT MODAL
      ====================================== */}

      {editingId !== null && (
        <div
          className="modal-overlay"
          onClick={cancelEditing}
        >

          <div
            className="edit-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            {/* MODAL HEADER */}

            <div className="edit-modal-header">

              <div>

                <p>
                  EDIT LISTING
                </p>

                <h2>
                  Edit Hostel Information
                </h2>

              </div>

              <button
                className="modal-close-button"
                onClick={cancelEditing}
              >
                ×
              </button>

            </div>

            {/* FORM */}

            <form onSubmit={handleUpdate}>

              {/* BASIC INFORMATION */}

              <div className="modal-form-section">

                <h3>
                  Basic Information
                </h3>

                <div className="modal-form-grid">

                  <div className="modal-field full-width">

                    <label>
                      Hostel Name
                    </label>

                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                    />

                  </div>

                  <div className="modal-field">

                    <label>
                      Location
                    </label>

                    <input
                      type="text"
                      name="location"
                      value={formData.location}
                      onChange={handleChange}
                      required
                    />

                  </div>

                  <div className="modal-field">

                    <label>
                      Monthly Rent
                    </label>

                    <input
                      type="number"
                      name="rent"
                      value={formData.rent}
                      onChange={handleChange}
                      min="0"
                      required
                    />

                  </div>

                  <div className="modal-field">

                    <label>
                      Room Type
                    </label>

                    <select
                      name="room_type"
                      value={formData.room_type}
                      onChange={handleChange}
                      required
                    >
                      <option value="">
                        Select room type
                      </option>

                      <option value="Shared">
                        Shared
                      </option>

                      <option value="Single">
                        Single
                      </option>

                      <option value="Double">
                        Double
                      </option>

                    </select>

                  </div>

                  <div className="modal-field">

                    <label>
                      Available Rooms
                    </label>

                    <input
                      type="number"
                      name="available_rooms"
                      value={
                        formData.available_rooms
                      }
                      onChange={handleChange}
                      min="0"
                      required
                    />

                  </div>

                </div>

              </div>

              {/* FACILITIES */}

              <div className="modal-form-section">

                <h3>
                  Facilities
                </h3>

                <div className="modal-field">

                  <label>
                    Facilities
                  </label>

                  <input
                    type="text"
                    name="facilities"
                    value={formData.facilities}
                    onChange={handleChange}
                    placeholder="WiFi, Mess, Heating"
                    required
                  />

                  <small>
                    Separate facilities with commas.
                  </small>

                </div>

              </div>

              {/* DESCRIPTION */}

              <div className="modal-form-section">

                <h3>
                  Description
                </h3>

                <div className="modal-field">

                  <label>
                    Hostel Description
                  </label>

                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    rows="4"
                    placeholder="Describe the hostel..."
                  />

                </div>

              </div>

              {/* OWNER */}

              <div className="modal-form-section">

                <h3>
                  Owner Information
                </h3>

                <div className="modal-form-grid">

                  <div className="modal-field">

                    <label>
                      Owner Name
                    </label>

                    <input
                      type="text"
                      name="owner_name"
                      value={formData.owner_name}
                      onChange={handleChange}
                    />

                  </div>

                  <div className="modal-field">

                    <label>
                      Owner Phone
                    </label>

                    <input
                      type="text"
                      name="owner_phone"
                      value={formData.owner_phone}
                      onChange={handleChange}
                    />

                  </div>

                </div>

              </div>

              {/* MODAL ACTIONS */}

              <div className="edit-modal-actions">

                <button
                  type="button"
                  className="cancel-edit-button"
                  onClick={cancelEditing}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="save-edit-button"
                >
                  Save Changes
                </button>

              </div>

            </form>

          </div>

        </div>
      )}

    </div>
  );
}

export default ManageListings;