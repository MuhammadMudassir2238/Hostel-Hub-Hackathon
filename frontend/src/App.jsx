import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/home";
import Search from "./pages/Search";
import Results from "./pages/Results";
import HostelDetails from "./pages/hostelDetails";
import Booking from "./pages/Booking";
import OwnerDashboard from "./pages/OwnerDashboard";
import MyBookings from "./pages/MyBookings";
import ManageListings from "./pages/Managelistings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/search" element={<Search />} />

        <Route path="/results" element={<Results />} />

        <Route path="hostels/:id" element={<HostelDetails />} />

        <Route path="/booking/:hostelId" element={<Booking />} />

        <Route path="/owner/dashboard" element={<OwnerDashboard />} />
        <Route path="/my-bookings" element={<MyBookings />} />
        <Route path="/owner/listings" element={<ManageListings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
